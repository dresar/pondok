# Dokumentasi Endpoints Aplikasi Core

Aplikasi `core` memiliki endpoint manajemen yang sangat banyak karena menangani hampir seluruh konten profil website.

Base URL: `/admin-panel/` (untuk view CRUD di bawah `core` app).

## Manajemen Konten Profil

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `visi-misi/` | `visi_misi_form` | Edit Visi Misi. |
| `sejarah-timeline/` | `sejarah_timeline_list` | CRUD Timeline Sejarah. |
| `kmi/` | `kmi_form` | Edit Profil KMI. |
| `fasilitas/` | `fasilitas_list` | CRUD Fasilitas. |
| `statistik/` | `statistik_list` | CRUD Statistik. |

## Manajemen Program & Pendidikan

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `program/` | `program_list` | CRUD Program Unggulan. |
| `program-pendidikan/` | `program_pendidikan_list` | CRUD Jenjang Pendidikan. |
| `ekstrakurikuler/` | `ekstrakurikuler_list` | CRUD Ekstrakurikuler. |
| `jadwal-harian/` | `jadwal_harian_list` | CRUD Jadwal Harian. |

## Manajemen Pendaftaran & Info

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `persyaratan/` | `persyaratan_form` | Edit Persyaratan. |
| `alur-pendaftaran/` | `alur_pendaftaran_form` | Edit Alur Pendaftaran. |
| `biaya-pendidikan/` | `biaya_pendidikan_list` | CRUD Biaya Pendidikan. |
| `informasi-tambahan/` | `informasi_tambahan_list` | CRUD Widget Informasi. |
| `seragam/` | `seragam_list` | CRUD Info Seragam. |

## Media & Galeri

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `media/` | `media_list` | CRUD Galeri & Video. |
| `dokumentasi/` | `dokumentasi_list` | CRUD Dokumentasi Kegiatan. |
| `hero-section/` | `hero_section_list` | CRUD Slider Homepage. |

## Komunikasi & Kontak

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `kontak/` | `kontak_list` | Inbox pesan masuk. |
| `faq/` | `faq_list` | CRUD FAQ. |
| `contact-person/` | `contact_person_list` | CRUD Panitia/CP. |
| `social-media/` | `social_media_list` | CRUD Social Media Footer. |
| `whatsapp-template/` | `whatsapp_template_list` | CRUD Template WA. |
| `whatsapp-broadcast/` | `whatsapp_broadcast` | Fitur Broadcast WA. |

## Public Endpoints

Endpoint publik diakses melalui aplikasi `public` (root URLs).

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `/` | `home` | Homepage website. |
| `/about/` | `about` | Halaman tentang pondok (deprecated/redirect). |
| `/tenaga-pengajar/` | `tenaga_pengajar_list` | Halaman daftar ustadz/ustadzah. |
| `/tenaga-pengajar/<id>/json/` | `tenaga_pengajar_detail_json` | API JSON detail pengajar. |
