# Dokumentasi Models Aplikasi Documents

Aplikasi `documents` menangani pembuatan dan manajemen dokumen dinamis (Surat Pernyataan, Form Pendaftaran, dll).

## 1. DocumentTemplate

Model untuk menyimpan template dokumen yang dapat dicustomisasi.

### Fields

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `nama` | CharField | Nama template dokumen. |
| `slug` | SlugField | Identifier unik template. |
| `deskripsi` | TextField | Deskripsi singkat. |
| `html_template` | TextField | Template konten HTML dengan support placeholder (misal: `{{nama_lengkap}}`). |
| `css_template` | TextField | CSS custom untuk styling PDF. |
| `ukuran_kertas` | CharField | Pilihan: `A4`, `Letter`, `Legal`. |
| `orientasi` | CharField | `portrait` atau `landscape`. |
| `margin_top` | CharField | Margin atas (default `1.5cm`). |
| `margin_right` | CharField | Margin kanan (default `1.5cm`). |
| `margin_bottom` | CharField | Margin bawah (default `1.5cm`). |
| `margin_left` | CharField | Margin kiri (default `1.5cm`). |
| `is_active` | BooleanField | Status aktif. |
| `order` | PositiveIntegerField | Urutan tampil. |

### Placeholder yang Didukung

Template HTML mendukung variabel placeholder yang akan diganti otomatis dengan data santri:
- `{{nama_lengkap}}`
- `{{nisn}}`
- `{{tempat_lahir}}`
- `{{tanggal_lahir}}`
- `{{alamat}}`
- Dan field santri lainnya.
