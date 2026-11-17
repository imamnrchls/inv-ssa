# Undangan Pernikahan Online

Halaman undangan satu file (`index.html`), tema maroon–krem: sampul dengan nama tamu, hitung mundur, ayat, profil mempelai, love story, akad & resepsi, live streaming, galeri, wedding gift (rekening + alamat, tombol salin), ucapan & konfirmasi kehadiran, dan penutup.

## Cara mengubah isi
Buka `index.html`, cari objek `CONFIG` di bagian `<script>`, lalu ubah nama, tanggal, lokasi, rekening, cerita, dan foto.

- **Foto**: taruh file di folder `img/`, lalu isi path-nya, mis. `photos: { cover: "img/cover.jpg", ... }`, `groom.photo`, `bride.photo`, `events[i].photo`, `gallery: [...]`. Foto yang kosong tampil sebagai placeholder.
- **Musik**: isi `music: "audio/lagu.mp3"`. Musik mulai saat tamu menekan "Buka Undangan".
- **Nama tamu / kirim undangan**: buka `/kirim` (mis. `https://sifayoga.web.id/kirim`), tempel daftar tamu (satu per baris, nomor WA opsional setelah koma), lalu tekan **Kirim WA** per tamu. Link berbentuk `/?to=Nama+Tamu`; nama tampil di sampul dan otomatis terisi di form ucapan.
- **Ucapan untuk semua tamu**: tanpa backend, ucapan hanya tersimpan di browser tamu itu sendiri. Pasang `apps-script.gs` di Google Sheets (langkah ada di bagian atas file itu), lalu isi `rsvpEndpoint` dengan Web app URL-nya. Ucapan bisa dihapus dengan menghapus barisnya di Sheet.

## Hosting
Aktifkan GitHub Pages (Settings → Pages → Deploy from branch) atau upload ke Netlify/Vercel. Tidak perlu proses build.

## Daftar tamu dari Excel
`tools/buat_link_tamu.py` membuat template Excel daftar tamu dan memprosesnya menjadi daftar link per tamu
dengan tombol "Kirim WA":

```
python tools/buat_link_tamu.py template "Template Daftar Tamu.xlsx"
python tools/buat_link_tamu.py proses "Daftar Tamu (terisi).xlsx" "Link Tamu.xlsx"
```
Domain undangan diatur di `DOMAIN` di dalam skrip. File Excel berisi data tamu sebaiknya tidak di-commit.
