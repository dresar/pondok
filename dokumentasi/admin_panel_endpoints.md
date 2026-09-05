# Dokumentasi Endpoints Aplikasi Admin Panel

Base URL: `/admin-panel/` (sesuai konfigurasi root URL proyek).

## Dashboard & Index

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `/` | `index` | Halaman utama dashboard admin panel. |

## Manajemen Santri

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `santri/` | `santri_list` | Daftar semua santri. |
| `santri/add/` | `santri_create` | Form tambah santri baru manual. |
| `santri/<id>/` | `santri_detail` | Detail data santri. |
| `santri/<id>/pdf/` | `santri_pdf` | Generate PDF data santri. |
| `santri/<id>/edit/` | `santri_update` | Form edit data santri. |
| `santri/<id>/delete/` | `santri_delete` | Hapus data santri. |
| `santri/<id>/update-status/` | `santri_update_status` | Update status pendaftaran santri. |
| `santri/export/` | `santri_export` | Export data santri (Excel/CSV). |
| `santri/import/` | `santri_import` | Import data santri. |
| `santri/bulk-action/` | `santri_bulk_action` | Aksi massal untuk data santri. |
| `santri/dokumen/` | `santri_dokumen_list` | Daftar dokumen santri. |
| `santri/<id>/approve-dokumen/` | `santri_approve_dokumen` | Approval dokumen santri. |
| `santri/<id>/json/` | `santri_json_detail` | Endpoint JSON detail santri. |
| `santri/search/` | `santri_search_api` | Endpoint pencarian santri. |

## Keuangan & Pembayaran

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `keuangan/` | `keuangan_dashboard` | Dashboard keuangan. |
| `keuangan/bank/` | `bank_account_list` | Daftar rekening bank. |
| `keuangan/bank/<id>/delete/` | `bank_account_delete` | Hapus rekening bank. |
| `pembayaran/` | `payment_list` | Daftar pembayaran. |
| `pembayaran/<id>/` | `payment_detail` | Detail pembayaran. |
| `pembayaran/<id>/verify/` | `payment_verify` | Verifikasi pembayaran. |
| `pembayaran/export/` | `payment_export` | Export data pembayaran. |
| `pembayaran/bulk-action/` | `payment_bulk_action` | Aksi massal pembayaran. |

## Manajemen User & Staff

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `santri/user-accounts/` | `user_account_list` | Daftar akun user santri. |
| `santri/user-accounts/create/` | `user_account_create` | Buat akun user baru. |
| `santri/user-accounts/<id>/edit/` | `user_account_update` | Edit akun user. |
| `santri/user-accounts/<id>/delete/` | `user_account_delete` | Hapus akun user. |
| `santri/user-accounts/<id>/change-password/` | `user_account_change_password` | Ubah password user. |
| `staff/` | `staff_list` | Daftar staff admin. |
| `staff/create/` | `staff_create` | Tambah staff baru. |
| `staff/<id>/edit/` | `staff_update` | Edit data staff. |
| `staff/<id>/delete/` | `staff_delete` | Hapus staff. |
| `staff/<id>/change-password/` | `staff_change_password` | Ubah password staff. |

## Tenaga Pengajar

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `tenaga-pengajar/` | `tenaga_pengajar_list` | Daftar tenaga pengajar. |
| `tenaga-pengajar/add/` | `tenaga_pengajar_create` | Tambah tenaga pengajar. |
| `tenaga-pengajar/<id>/` | `tenaga_pengajar_detail` | Detail tenaga pengajar. |
| `tenaga-pengajar/<id>/edit/` | `tenaga_pengajar_update` | Edit tenaga pengajar. |
| `tenaga-pengajar/<id>/delete/` | `tenaga_pengajar_delete` | Hapus tenaga pengajar. |
| `tenaga-pengajar/bagian/` | `bagian_jabatan_list` | Manajemen bagian/jabatan. |

## Tools & Settings

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `settings/` | `settings` | Pengaturan website umum. |
| `settings/users/` | `user_settings` | Pengaturan user. |
| `profile/` | `user_profile` | Profil user login saat ini. |
| `login-statistics/` | `login_statistics` | Statistik login user. |
| `tools/image-converter/` | `image_converter` | Alat konversi gambar. |
| `tools/converted-images/` | `converted_image_list` | Galeri gambar hasil konversi. |
| `tools/media-files/` | `media_files_manager` | File manager media. |
| `bug-notes/` | `bug_note_list` | Daftar catatan bug. |
