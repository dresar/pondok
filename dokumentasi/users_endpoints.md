# Dokumentasi Endpoints Aplikasi Users

Base URL: `/users/`.

## Autentikasi

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `login/` | `login` | Halaman login user & admin. |
| `register/` | `register` | Halaman registrasi akun baru. |
| `logout/` | `logout` | Proses logout. |

## Dashboard & Profil (User Area)

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `dashboard/` | `dashboard` | Halaman utama dashboard user santri. |
| `profile/` | `profile` | Edit profil user. |
| `profile/change-password/` | `change_password` | Ubah password. |
| `riwayat/` | `riwayat` | Riwayat aktivitas/log user. |
| `notifikasi/` | `notifikasi` | Halaman notifikasi user. |

## Fitur Santri (User Area)

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `pendaftaran/` | `pendaftaran` | Form data diri santri (wizard/steps). |
| `pendaftaran/pdf/` | `pendaftaran_pdf` | Download bukti pendaftaran PDF. |
| `status/` | `status` | Cek status kelulusan/pendaftaran. |
| `dokumen/` | `dokumen` | Halaman kelola dokumen santri. |
| `dokumen/upload/<type>/` | `dokumen_upload` | Upload dokumen spesifik (ktp, akta, dll). |
| `dokumen/download/<type>/` | `dokumen_download` | Download file dokumen yang sudah diupload. |
| `pembayaran/` | `pembayaran` | Halaman status pembayaran & upload bukti. |
