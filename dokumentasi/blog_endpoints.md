# Dokumentasi Endpoints Aplikasi Blog

Base URL: `/blog/` (untuk manajemen/admin) dan `/` (untuk public).

## Manajemen (Admin Panel)

Endpoint ini digunakan untuk manajemen konten blog via Admin Panel (bukan Django Admin bawaan).

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `/` | `list` | Daftar semua artikel blog. |
| `add/` | `create` | Form tambah artikel baru. |
| `<id>/` | `detail` | Detail artikel. |
| `<id>/edit/` | `update` | Edit artikel. |
| `<id>/delete/` | `delete` | Hapus artikel. |
| `<id>/like/` | `increment_likes` | Endpoint increment like. |
| `<id>/share/` | `increment_shares` | Endpoint increment share. |

### Kategori & Tag Management

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `category/` | `category_list` | Daftar kategori. |
| `category/add/` | `category_create` | Tambah kategori. |
| `category/<id>/edit/` | `category_update` | Edit kategori. |
| `category/<id>/delete/` | `category_delete` | Hapus kategori. |
| `tag/` | `tag_list` | Daftar tag. |
| `tag/add/` | `tag_create` | Tambah tag. |
| `tag/<id>/edit/` | `tag_update` | Edit tag. |
| `tag/<id>/delete/` | `tag_delete` | Hapus tag. |

### Testimoni & Pengumuman Management

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `testimoni/` | `testimoni_list` | Daftar testimoni. |
| `testimoni/add/` | `testimoni_create` | Tambah testimoni. |
| `testimoni/<id>/edit/` | `testimoni_update` | Edit testimoni. |
| `testimoni/<id>/delete/` | `testimoni_delete` | Hapus testimoni. |
| `pengumuman/` | `pengumuman_list` | Daftar pengumuman. |
| `pengumuman/add/` | `pengumuman_create` | Tambah pengumuman. |
| `pengumuman/<id>/edit/` | `pengumuman_update` | Edit pengumuman. |
| `pengumuman/<id>/delete/` | `pengumuman_delete` | Hapus pengumuman. |

## Public Endpoints

Endpoint ini diakses oleh pengunjung website (via aplikasi `core/urls_public.py` namun menggunakan view dari blog).

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `/blog/` | `public:blog_list` | Halaman daftar artikel blog publik. |
| `/blog/<slug>/` | `public:blog_detail` | Halaman baca artikel detail publik. |
