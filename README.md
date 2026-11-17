# Undangan Pernikahan Online

Halaman undangan satu file (`index.html`), tema maroon–krem: sampul dengan nama tamu, hitung mundur, ayat, profil mempelai, love story, akad & resepsi, live streaming, galeri, wedding gift (rekening + alamat, tombol salin), ucapan & konfirmasi kehadiran, dan penutup.

## Cara mengubah isi
Buka `index.html`, cari objek `CONFIG` di bagian `<script>`, lalu ubah nama, tanggal, lokasi, rekening, cerita, dan foto.

- **Foto**: taruh file di folder `img/`, lalu isi path-nya, mis. `photos: { cover: "img/cover.jpg", ... }`, `groom.photo`, `bride.photo`, `events[i].photo`, `gallery: [...]`. Foto yang kosong tampil sebagai placeholder.
- **Musik**: isi `music: "audio/lagu.mp3"`. Musik mulai saat tamu menekan "Buka Undangan".
- **Nama tamu**: kirim link dengan `?to=Nama+Tamu`, mis. `https://domain-anda/?to=Budi+Santoso`.
- **Ucapan untuk semua tamu**: tanpa backend, ucapan hanya tersimpan di browser tamu itu sendiri. Agar ucapan bisa dilihat semua orang, pasang `apps-script.gs` di Google Sheets (petunjuk di dalam file) dan isi `rsvpEndpoint`.

## Hosting
Aktifkan GitHub Pages (Settings → Pages → Deploy from branch) atau upload ke Netlify/Vercel. Tidak perlu proses build.
