"""Buat template daftar tamu, atau proses daftar tamu yang sudah diisi menjadi link per tamu.

  python tools/buat_link_tamu.py template  OUT.xlsx [--contoh "Nama" "08xx"]
  python tools/buat_link_tamu.py proses    IN.xlsx OUT.xlsx

Hasil proses: satu baris per tamu berisi link undangan, nomor WA (format 62), tombol
"Kirim WA" (link wa.me dengan pesan terisi) dan teks pesan lengkap.
"""
import re, sys
from urllib.parse import quote
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

DOMAIN = "https://sifayoga.web.id"
DEFAULT_MSG = """Assalamu'alaikum Warahmatullahi Wabarakatuh

Kepada Yth.
Bapak/Ibu/Saudara/i *{nama}*

Tanpa mengurangi rasa hormat, perkenankan kami mengundang Bapak/Ibu/Saudara/i untuk menghadiri acara pernikahan kami:

*Sifa & Yoga*
Minggu, 27 Desember 2026
Sakha Ballroom, Royal Sentul Park

Info lengkap acara dan konfirmasi kehadiran:
{link}

Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.

Wassalamu'alaikum Warahmatullahi Wabarakatuh

Kami yang berbahagia,
Sifa & Yoga"""

WINE = "4A0F1C"; CREAM = "EDE6DD"; GOLD = "E9D9C6"
F = "Arial"
HEAD = Font(name=F, bold=True, color="FFFFFF", size=11)
HEAD_FILL = PatternFill("solid", fgColor=WINE)
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")   # yellow-ish: cells to fill in
THIN = Side(style="thin", color="D9CBBB")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def link_for(name: str) -> str:
    return f"{DOMAIN}/?to=" + quote(name.strip(), safe="").replace("%20", "+")


def wa_number(raw) -> str:
    d = re.sub(r"\D", "", str(raw or ""))
    if not d:
        return ""
    if d.startswith("0"):
        d = "62" + d[1:]
    elif d.startswith("8"):
        d = "62" + d
    return d


def style_header(ws, headers, widths):
    for i, (h, w) in enumerate(zip(headers, widths), 1):
        c = ws.cell(row=1, column=i, value=h)
        c.font, c.fill, c.border = HEAD, HEAD_FILL, BOX
        c.alignment = Alignment(vertical="center", horizontal="center", wrap_text=True)
        ws.column_dimensions[c.column_letter].width = w
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"


def make_template(out, example=None, rows=300):
    wb = Workbook()
    ws = wb.active; ws.title = "Daftar Tamu"
    style_header(ws, ["No", "Nama Tamu\n(tampil di undangan)", "No. WhatsApp", "Kategori\n(opsional)", "Link Undangan\n(otomatis)"],
                 [6, 42, 20, 20, 60])
    body = Font(name=F, size=11)
    for r in range(2, rows + 2):
        ws.cell(row=r, column=1, value=f'=IF(B{r}="","",ROW()-1)').font = body
        for col in (2, 3, 4):
            c = ws.cell(row=r, column=col); c.fill, c.border, c.font = INPUT_FILL, BOX, body
        ws.cell(row=r, column=3).number_format = "@"   # keep the leading 0 of phone numbers
        # Link formula: encode the few characters that break a URL, spaces become +.
        name = f'TRIM(B{r})'
        enc = f'SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE({name},"%","%25"),"&","%26"),"#","%23"),"+","%2B")," ","+")'
        c = ws.cell(row=r, column=5, value=f'=IF(B{r}="","","{DOMAIN}/?to="&{enc})')
        c.font = Font(name=F, size=10, color="4A0F1C")
    if example:
        ws["B2"], ws["C2"], ws["D2"] = example[0], example[1], "Contoh / uji coba"
    dv = DataValidation(type="textLength", operator="lessThanOrEqual", formula1="80", allow_blank=True,
                        error="Nama maksimal 80 karakter.", errorTitle="Nama terlalu panjang")
    ws.add_data_validation(dv); dv.add(f"B2:B{rows + 1}")

    pm = wb.create_sheet("Pesan WA")
    style_header(pm, ["Template pesan WhatsApp — {nama} dan {link} diganti otomatis"], [90])
    c = pm["A2"]; c.value = DEFAULT_MSG; c.fill = INPUT_FILL; c.font = Font(name=F, size=11)
    c.alignment = Alignment(wrap_text=True, vertical="top"); pm.row_dimensions[2].height = 420

    hp = wb.create_sheet("Petunjuk")
    hp.column_dimensions["A"].width = 100
    lines = [
        ("Cara mengisi", True),
        ("1. Isi hanya sel berwarna kuning di tab 'Daftar Tamu': Nama Tamu, No. WhatsApp, dan Kategori (opsional).", False),
        ("2. Nama Tamu ditulis persis seperti yang ingin tampil di undangan, mis. 'Bapak Budi Santoso & Keluarga'.", False),
        ("3. No. WhatsApp boleh 08xx, +62xx, atau pakai spasi/tanda hubung. Kosongkan jika tidak ada.", False),
        ("4. Kolom 'Link Undangan' terisi otomatis — bisa langsung disalin dan dikirim manual.", False),
        ("5. Teks pesan bisa diubah di tab 'Pesan WA'. Biarkan {nama} dan {link} di dalam pesan.", False),
        ("6. Baris 2 adalah contoh / uji coba — boleh ditimpa atau dihapus.", False),
        ("", False),
        ("Setelah selesai", True),
        ("Kirim file ini kembali. Hasilnya berupa daftar dengan tombol 'Kirim WA' per tamu: klik, WhatsApp terbuka", False),
        ("ke nomor tamu dengan pesan undangan yang sudah terisi, tinggal tekan kirim.", False),
    ]
    for i, (t, b) in enumerate(lines, 1):
        cell = hp.cell(row=i, column=1, value=t); cell.font = Font(name=F, size=11, bold=b, color=WINE if b else "000000")
    wb.active = 0
    wb.save(out)


def process(src, out):
    wb = load_workbook(src, data_only=True)
    ws = wb["Daftar Tamu"]
    msg_tpl = (wb["Pesan WA"]["A2"].value if "Pesan WA" in wb.sheetnames else None) or DEFAULT_MSG
    guests, seen, skipped = [], set(), []
    for r in range(2, ws.max_row + 1):
        name = str(ws.cell(row=r, column=2).value or "").strip()
        if not name:
            continue
        if name.lower() in seen:
            skipped.append(f"baris {r}: '{name}' duplikat"); continue
        seen.add(name.lower())
        guests.append((name, ws.cell(row=r, column=3).value, str(ws.cell(row=r, column=4).value or "").strip()))

    o = Workbook(); s = o.active; s.title = "Link Tamu"
    style_header(s, ["No", "Nama Tamu", "Kategori", "No. WA (62)", "Kirim WA", "Link Undangan", "Pesan WA", "Terkirim?"],
                 [6, 36, 18, 18, 14, 55, 70, 12])
    body = Font(name=F, size=11)
    for i, (name, phone, cat) in enumerate(guests, 1):
        r = i + 1
        link, num = link_for(name), wa_number(phone)
        text = msg_tpl.replace("{nama}", name).replace("{link}", link)
        wa = (f"https://wa.me/{num}" if num else "https://wa.me/") + "?text=" + quote(text, safe="")
        vals = [i, name, cat, num, "Kirim WA", link, text, ""]
        for col, v in enumerate(vals, 1):
            c = s.cell(row=r, column=col, value=v); c.font, c.border = body, BOX
            c.alignment = Alignment(vertical="top", wrap_text=(col == 7))
        s.cell(row=r, column=4).number_format = "@"
        k = s.cell(row=r, column=5); k.hyperlink = wa
        k.font = Font(name=F, size=11, bold=True, color="FFFFFF"); k.fill = PatternFill("solid", fgColor="1F7A4D")
        k.alignment = Alignment(horizontal="center", vertical="top")
        l = s.cell(row=r, column=6); l.hyperlink = link; l.font = Font(name=F, size=10, color=WINE, underline="single")
        s.cell(row=r, column=8).fill = INPUT_FILL
        s.row_dimensions[r].height = 18
    note = s.cell(row=len(guests) + 3, column=2,
                  value="Klik 'Kirim WA' untuk membuka WhatsApp dengan pesan terisi. Tamu tanpa nomor: WhatsApp meminta Anda memilih kontak. Tandai kolom 'Terkirim?' setelah mengirim.")
    note.font = Font(name=F, size=10, italic=True, color="6F6264")
    o.save(out)
    return guests, skipped


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "template":
        ex = None
        if "--contoh" in sys.argv:
            i = sys.argv.index("--contoh"); ex = (sys.argv[i + 1], sys.argv[i + 2])
        make_template(sys.argv[2], ex)
    elif cmd == "proses":
        g, sk = process(sys.argv[2], sys.argv[3])
        print(f"{len(g)} tamu diproses"); [print(" -", x) for x in sk]
