# Dokumentasi Models Aplikasi Admin Panel

Aplikasi `admin_panel` memiliki beberapa model khusus untuk kebutuhan manajemen internal.

## 1. ConvertedImage

Model ini digunakan untuk menyimpan gambar yang telah dikonversi ke format WebP untuk optimasi performa.

### Fields

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `judul` | CharField | Judul gambar untuk pencarian (max 200 char). Default kosong. |
| `original_filename` | CharField | Nama file asli sebelum dikonversi (max 255 char). |
| `webp_image` | ImageField | File gambar hasil konversi WebP. Upload ke `converted/%Y/%m/%d/`. |
| `original_size` | BigIntegerField | Ukuran file asli dalam bytes. |
| `converted_size` | BigIntegerField | Ukuran file WebP dalam bytes. |
| `compression_ratio` | FloatField | Persentase rasio kompresi. |
| `quality` | IntegerField | Kualitas konversi WebP (default 85). |
| `width` | IntegerField | Lebar gambar dalam pixel (nullable). |
| `height` | IntegerField | Tinggi gambar dalam pixel (nullable). |
| `created_by` | ForeignKey | User yang melakukan konversi (relasi ke `User`). |
| `created_at` | DateTimeField | Waktu pembuatan (auto_now_add). |

### Methods

- `get_original_size_mb()`: Mengembalikan ukuran asli dalam MB.
- `get_converted_size_kb()`: Mengembalikan ukuran WebP dalam KB.
- `get_savings_mb()`: Mengembalikan jumlah penghematan ukuran dalam MB.
- `get_cdn_url()`: Mengembalikan URL publik gambar.

## 2. BugNote

Model sederhana untuk mencatat bug atau todo list bagi admin panel.

### Fields

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `title` | CharField | Judul catatan (max 200 char). |
| `description` | TextField | Deskripsi detail bug/catatan. |
| `page_url` | URLField | URL halaman dimana bug ditemukan. |
| `status` | CharField | Status bug: `open`, `progress`, `closed`. Default `open`. |
| `created_by` | ForeignKey | User pembuat catatan. |
| `created_at` | DateTimeField | Waktu pembuatan. |

### Choices (Status)

- `open`: Open
- `progress`: In Progress
- `closed`: Closed
