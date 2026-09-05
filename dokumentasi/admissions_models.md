# Dokumentasi Models Aplikasi Admissions

Aplikasi `admissions` menangani proses pendaftaran santri baru.

## 1. Santri

Model utama yang menyimpan seluruh data pendaftaran calon santri.

### Data Pribadi

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `nama_lengkap` | CharField | Nama lengkap santri. |
| `nama_panggilan` | CharField | Nama panggilan (opsional). |
| `nisn` | CharField | Nomor Induk Siswa Nasional (10 digit, unique). |
| `tempat_lahir` | CharField | Tempat lahir. |
| `tanggal_lahir` | DateField | Tanggal lahir. |
| `jenis_kelamin` | CharField | `L` (Laki-laki) atau `P` (Perempuan). |
| `agama` | CharField | Default 'Islam'. |
| `kewarganegaraan` | CharField | `WNI` atau `WNA`. |
| `anak_ke` | PositiveIntegerField | Urutan anak dalam keluarga. |
| `jumlah_saudara` | PositiveIntegerField | Jumlah saudara kandung. |
| `bahasa_sehari_hari` | CharField | Bahasa yang digunakan sehari-hari. |
| `golongan_darah` | CharField | Pilihan: A, B, AB, O. |
| `tinggi_badan` | PositiveIntegerField | Dalam cm. |
| `berat_badan` | PositiveIntegerField | Dalam kg. |
| `riwayat_penyakit` | CharField | Riwayat penyakit jika ada. |
| `tinggal_dengan` | CharField | Orang Tua, Wali, atau Lainnya. |

### Data Orang Tua (Ayah & Ibu)

Terdapat field serupa untuk Ayah dan Ibu dengan suffix `_ayah` dan `_ibu`.

| Field Base | Keterangan |
|------------|------------|
| `nama` | Nama orang tua. |
| `nik` | NIK KTP (16 digit). |
| `tempat_lahir` | Tempat lahir. |
| `tanggal_lahir` | Tanggal lahir. |
| `agama` | Agama. |
| `kewarganegaraan` | WNI/WNA. |
| `pendidikan` | SD s/d S3. |
| `pekerjaan` | Pekerjaan saat ini. |
| `no_hp` | Nomor Handphone. |
| `status` | HIDUP atau MENINGGAL. |
| `alamat_orangtua` | Alamat lengkap orang tua. |

### Kontak & Alamat Santri

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `alamat` | TextField | Alamat lengkap domisili. |
| `desa` | CharField | Desa/Kelurahan. |
| `kecamatan` | CharField | Kecamatan. |
| `kabupaten` | CharField | Kabupaten/Kota. |
| `provinsi` | CharField | Provinsi. |
| `kode_pos` | CharField | Kode Pos. |
| `no_hp` | CharField | Nomor HP Santri/Wali yang bisa dihubungi. |
| `email` | EmailField | Alamat email (opsional). |

### Data Sekolah Asal

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `asal_sekolah` | CharField | Nama sekolah sebelumnya. |
| `npsn_sekolah` | CharField | NPSN sekolah asal. |
| `kelas_terakhir` | CharField | Kelas terakhir yang diduduki. |
| `tahun_lulus` | CharField | Tahun kelulusan. |
| `no_ijazah` | CharField | Nomor Ijazah/SKHUN. |
| `kelas_diterima` | CharField | Kelas yang akan dimasuki di pesantren. |
| `tanggal_diterima` | DateField | Tanggal resmi diterima. |

### Dokumen Upload

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `foto_santri` | ImageField | Upload foto santri. |
| `foto_ktp` | ImageField | Upload KTP/KK. |
| `foto_akta` | ImageField | Upload Akta Kelahiran. |
| `foto_ijazah` | ImageField | Upload Ijazah/SKHUN. |
| `surat_sehat` | ImageField | Upload Surat Keterangan Sehat. |

### Status Approval Dokumen

Field boolean untuk menandai persetujuan dokumen: `foto_santri_approved`, `foto_ktp_approved`, `foto_akta_approved`, `foto_ijazah_approved`, `surat_sehat_approved`.

### Status Pendaftaran

| Status | Keterangan |
|--------|------------|
| `pending` | Menunggu Verifikasi. |
| `verified` | Pembayaran Terverifikasi. |
| `accepted` | Diterima. |
| `rejected` | Ditolak. |

### Timestamps

- `created_at`: Tanggal daftar.
- `updated_at`: Terakhir diupdate.
