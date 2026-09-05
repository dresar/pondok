# Dokumentasi Endpoints Aplikasi Documents

Aplikasi `documents` menyediakan fitur untuk generate dokumen dan export data.

Base URL: `/documents/` (untuk fitur admin/staff) dan `/users/dokumen/` (untuk santri).

## Manajemen Dokumen (Admin/Staff)

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `/` | `list` | Daftar santri untuk export dokumen/Excel. |
| `tutorial/` | `tutorial` | Halaman tutorial mail merge. |
| `generate/` | `generate_excel` | Generate Excel semua santri untuk Mail Merge. |
| `generate/<id>/` | `generate_excel_single` | Generate Excel untuk satu santri. |

## Akses Dokumen Santri (User)

Endpoint ini diakses melalui aplikasi `users`.

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `/users/dokumen/` | `users:dokumen` | Halaman dokumen santri. |
| `/users/dokumen/download/<type>/` | `users:dokumen_download` | Download dokumen spesifik. |
