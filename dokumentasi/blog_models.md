# Dokumentasi Models Aplikasi Blog

Aplikasi `blog` menangani manajemen artikel, pengumuman, dan testimoni.

## 1. Category

Kategori untuk mengelompokkan artikel blog.

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `name` | CharField | Nama kategori (unique). |
| `slug` | SlugField | Slug URL (unique). |
| `order` | PositiveIntegerField | Urutan tampil. |

## 2. Tag

Tag atau label untuk artikel blog.

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `name` | CharField | Nama tag (unique). |
| `slug` | SlugField | Slug URL (unique). |
| `order` | PositiveIntegerField | Urutan tampil. |

## 3. BlogPost

Model utama untuk artikel/berita.

### Fields

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `title` | CharField | Judul artikel. |
| `slug` | SlugField | Slug URL (unique). |
| `author` | ForeignKey | Penulis (User). |
| `content` | TextField | Isi artikel. |
| `excerpt` | TextField | Ringkasan singkat. |
| `featured_image` | ImageField | Gambar utama artikel. |
| `category` | ForeignKey | Kategori artikel. |
| `tags` | ManyToManyField | Tag artikel. |
| `meta_title` | CharField | Judul SEO. |
| `meta_description` | TextField | Deskripsi SEO. |
| `meta_keywords` | CharField | Keyword SEO. |
| `video_file` | FileField | File video jika ada. |
| `views_count` | PositiveIntegerField | Jumlah dilihat. |
| `likes_count` | PositiveIntegerField | Jumlah disukai. |
| `shares_count` | PositiveIntegerField | Jumlah dibagikan. |
| `status` | CharField | `draft`, `published`, `archived`. |
| `published_at` | DateTimeField | Tanggal publikasi. |
| `is_featured` | BooleanField | Menandai artikel unggulan. |

## 4. Testimoni

Model untuk menyimpan testimoni dari alumni atau wali santri.

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `nama` | CharField | Nama pemberi testimoni. |
| `foto` | ImageField | Foto profil. |
| `jabatan` | CharField | Jabatan atau status (misal: Alumni 2020). |
| `testimoni` | TextField | Isi testimoni. |
| `rating` | PositiveIntegerField | Rating 1-5. |
| `is_published` | BooleanField | Status publikasi. |
| `order` | PositiveIntegerField | Urutan tampil. |

## 5. Pengumuman

Model untuk pengumuman penting pesantren.

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `judul` | CharField | Judul pengumuman. |
| `slug` | SlugField | Slug URL. |
| `konten` | TextField | Isi pengumuman. |
| `gambar` | ImageField | Gambar pendukung. |
| `status` | CharField | `draft`, `published`. |
| `is_penting` | BooleanField | Menandai pengumuman penting/prioritas. |
| `published_at` | DateTimeField | Tanggal publikasi. |
| `meta_title` | CharField | Judul SEO. |
| `meta_description` | TextField | Deskripsi SEO. |
