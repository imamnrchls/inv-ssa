"""Buat satu file Excel daftar tamu: isi tab "Daftar Tamu", tab "Hasil Link" terisi otomatis.

  python tools/buat_link_tamu.py OUT.xlsx [--contoh "Nama" "08xx"]

Tab "Hasil Link" memakai rumus saja, jadi langsung bekerja di Excel, Google Sheets dan Excel HP.
Tombol "Kirim WA" mengarah ke /wa di situs undangan, yang menyusun pesan WhatsApp lalu membuka
WhatsApp (link wa.me berisi pesan lengkap terlalu panjang untuk rumus HYPERLINK di Excel).
"""
import sys
from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

DOMAIN = "https://sifayoga.web.id"
ROWS = 500

WINE = "4A0F1C"
F = "Arial"
HEAD = Font(name=F, bold=True, color="FFFFFF", size=11)
HEAD_FILL = PatternFill("solid", fgColor=WINE)
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
THIN = Side(style="thin", color="D9CBBB")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BODY = Font(name=F, size=11)


def header(ws, cols):
    for i, (title, width) in enumerate(cols, 1):
        c = ws.cell(row=1, column=i, value=title)
        c.font, c.fill, c.border = HEAD, HEAD_FILL, BOX
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[c.column_letter].width = width
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "A2"


def build(out, example=None):
    wb = Workbook()

    # ---- Daftar Tamu (input) ----
    d = wb.active
    d.title = "Daftar Tamu"
    header(d, [("No", 6), ("Nama Tamu\n(tampil di undangan)", 42), ("No. WhatsApp", 20),
               ("Kategori\n(opsional)", 18), ("Sudah dikirim?\n(isi: Ya)", 16)])
    for r in range(2, ROWS + 2):
        d.cell(row=r, column=1, value=f'=IF(B{r}="","",ROW()-1)').font = BODY
        for col in (2, 3, 4, 5):
            c = d.cell(row=r, column=col)
            c.fill, c.border, c.font = INPUT_FILL, BOX, BODY
        d.cell(row=r, column=3).number_format = "@"  # keep the leading 0
    if example:
        d["B2"], d["C2"], d["D2"] = example[0], example[1], "Uji coba"
    dv = DataValidation(type="textLength", operator="lessThanOrEqual", formula1="80", allow_blank=True,
                        errorTitle="Nama terlalu panjang", error="Nama tamu maksimal 80 karakter.")
    d.add_data_validation(dv)
    dv.add(f"B2:B{ROWS + 1}")
    sent = DataValidation(type="list", formula1='"Ya,Belum"', allow_blank=True)
    d.add_data_validation(sent)
    sent.add(f"E2:E{ROWS + 1}")

    # ---- Hasil Link (formulas only) ----
    h = wb.create_sheet("Hasil Link")
    header(h, [("No", 6), ("Nama Tamu", 36), ("Kategori", 16), ("No. WA (62)", 18),
               ("Kirim WA", 14), ("Link Undangan", 58), ("Sudah dikirim?", 14)])
    src = "'Daftar Tamu'!"
    for r in range(2, ROWS + 2):
        name = f"TRIM({src}B{r})"
        # URL-encode the characters that would break the query string; spaces become +.
        enc = (f'SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE({name},"%","%25"),'
               f'"&","%26"),"#","%23"),"+","%2B")," ","+")')
        # Phone: drop spaces, dashes, dots, brackets and +, then 08.. -> 628.., 8.. -> 628..
        digits = (f'SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE('
                  f'TRIM({src}C{r})," ",""),"-",""),".",""),"(",""),")",""),"+","")')
        blank = f'{src}B{r}=""'
        h.cell(row=r, column=1, value=f'=IF({blank},"",ROW()-1)')
        h.cell(row=r, column=2, value=f'=IF({blank},"",{name})')
        h.cell(row=r, column=3, value=f'=IF({blank},"",{src}D{r}&"")')
        h.cell(row=r, column=4, value=(f'=IF(OR({blank},{src}C{r}=""),"",IF(LEFT({digits},1)="0","62"&MID({digits},2,30),'
                                       f'IF(LEFT({digits},1)="8","62"&{digits},{digits})))'))
        h.cell(row=r, column=5, value=f'=IF({blank},"",HYPERLINK("{DOMAIN}/wa?n="&D{r}&"&to="&{enc},"Kirim WA"))')
        h.cell(row=r, column=6, value=f'=IF({blank},"",HYPERLINK("{DOMAIN}/?to="&{enc},"{DOMAIN}/?to="&{enc}))')
        h.cell(row=r, column=7, value=f'=IF({blank},"",IF({src}E{r}="","Belum",{src}E{r}))')
        for col in range(1, 8):
            c = h.cell(row=r, column=col)
            c.font = BODY
            c.border = BOX
        h.cell(row=r, column=4).number_format = "@"
        h.cell(row=r, column=5).font = Font(name=F, size=11, bold=True, color="1F7A4D", underline="single")
        h.cell(row=r, column=5).alignment = Alignment(horizontal="center")
        h.cell(row=r, column=6).font = Font(name=F, size=10, color=WINE, underline="single")
    rng = f"A2:G{ROWS + 1}"
    h.conditional_formatting.add(rng, FormulaRule(formula=['$G2="Ya"'], fill=PatternFill("solid", fgColor="E2F0E6")))

    # ---- Petunjuk ----
    p = wb.create_sheet("Petunjuk")
    p.column_dimensions["A"].width = 105
    lines = [
        ("Cara pakai", True),
        ("1. Buka tab 'Daftar Tamu' dan isi hanya sel berwarna kuning.", False),
        ("     - Nama Tamu: persis seperti yang ingin tampil di undangan, mis. 'Bapak Budi Santoso & Keluarga'.", False),
        ("     - No. WhatsApp: boleh 08xx, +62xx, atau pakai spasi/tanda hubung. Kosongkan jika tidak ada.", False),
        ("     - Kategori: opsional, mis. Keluarga / Kantor / Teman.", False),
        ("2. Tab 'Hasil Link' terisi otomatis untuk setiap nama.", False),
        ("3. Klik 'Kirim WA' di tab 'Hasil Link': WhatsApp terbuka ke nomor tamu dengan pesan undangan sudah terisi.", False),
        ("     Tamu tanpa nomor: WhatsApp meminta Anda memilih kontak.", False),
        ("4. Setelah terkirim, isi 'Ya' di kolom 'Sudah dikirim?' pada tab 'Daftar Tamu'. Barisnya di 'Hasil Link' jadi hijau.", False),
        ("5. Baris 2 adalah uji coba dan boleh ditimpa. Kapasitas 500 tamu.", False),
        ("", False),
        ("Catatan", True),
        ("- Jangan menyisipkan atau mengurutkan baris di 'Hasil Link'; cukup kelola daftar di tab 'Daftar Tamu'.", False),
        ("- Teks pesan WhatsApp diatur di situs undangan (halaman /wa). Minta perubahan teks bila perlu.", False),
        ("- Bisa dibuka di Excel, Excel HP, maupun Google Sheets.", False),
    ]
    for i, (t, bold) in enumerate(lines, 1):
        p.cell(row=i, column=1, value=t).font = Font(name=F, size=11, bold=bold, color=WINE if bold else "000000")

    wb.active = 0
    wb.save(out)


if __name__ == "__main__":
    ex = None
    if "--contoh" in sys.argv:
        i = sys.argv.index("--contoh")
        ex = (sys.argv[i + 1], sys.argv[i + 2])
    build(sys.argv[1], ex)
