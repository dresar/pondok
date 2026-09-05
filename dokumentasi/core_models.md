# Dokumentasi Models Aplikasi Core

Aplikasi `core` menyimpan model-model inti yang digunakan untuk pengaturan website, profil pondok, dan konten statis/dinamis lainnya.

## 1. WebsiteSettings (Singleton)

Pengaturan global website.

| Field | Keterangan |
|-------|------------|
| `nama_pondok` | Nama resmi pondok pesantren. |
| `arabic_name` | Nama dalam bahasa Arab. |
| `alamat`, `no_telepon`, `email` | Kontak utama. |
| `website`, `facebook`, `instagram`, `twitter`, `tiktok` | Link sosial media utama. |
| `logo`, `favicon`, `header_mobile_image` | Aset gambar identitas. |
| `hero_title`, `hero_subtitle`, `hero_tagline` | Teks utama di halaman depan. |
| `google_maps_embed_code` | Kode embed peta. |
| `maintenance_mode` | Toggle mode perbaikan website. |

## 2. Profil & Konten Statis

Model-model ini umumnya bersifat Singleton (hanya 1 record) atau list statis.

- **VisiMisi**: Menyimpan teks Visi dan Misi (HTML).
- **SejarahTimeline**: Timeline sejarah perkembangan pondok.
    - Relasi: `SejarahTimelineImage` (Galeri per timeline).
- **KMI**: Visi dan Profil KMI (Kulliyatu-l-Mu'allimin Al-Islamiyah).
- **Persyaratan**: Persyaratan penerimaan santri/santriwati (HTML).
- **AlurPendaftaran**: Penjelasan alur pendaftaran dan tahapan tes (HTML).

## 3. Program & Akademik

- **Program**: Program/kegiatan unggulan pondok.
- **ProgramPendidikan**: Jenjang pendidikan (SDIT, MTs, MA, dll).
    - Relasi: `ProgramPendidikanImage`.
- **Ekstrakurikuler**: Kegiatan ekstrakurikuler.
    - Relasi: `EkstrakurikulerImage`.
- **Fasilitas**: Fasilitas yang tersedia.
- **JadwalHarian**: Jadwal aktivitas santri/santriwati.
- **BiayaPendidikan**: Rincian biaya (Bulanan, Tahunan, Perlengkapan).
- **Seragam**: Informasi seragam santri/santriwati.

## 4. Manajemen Tenaga Pengajar

- **BagianJabatan**: Master data jabatan/bagian (Kepala Sekolah, Ustadz, dll).
- **TenagaPengajar**: Data lengkap ustadz/ustadzah.
    - Fields: Nama, Biodata, Pendidikan, Pengalaman, Medsos, dll.

## 5. Media & Informasi

- **Media**: Galeri foto dan video kegiatan.
- **Dokumentasi**: Rekam jejak kegiatan (Event/Acara).
    - Relasi: `DokumentasiImage`.
- **Statistik**: Angka statistik (Jumlah Santri, Luas Lahan, dll).
- **FAQ**: Pertanyaan yang sering diajukan.
- **InformasiTambahan**: Info widget (Waktu Pendaftaran, Dokumen, dll).

## 6. Kontak & Komunikasi

- **Kontak**: Inbox pesan dari form "Hubungi Kami".
- **ContactPerson**: Panitia yang bisa dihubungi (WhatsApp).
- **SocialMedia**: Link social media footer.
- **WhatsAppTemplate**: Template pesan WA (Public & System).
- **WhatsAppTemplateKategori**: Kategori template WA.
