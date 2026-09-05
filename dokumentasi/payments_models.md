# Dokumentasi Models Aplikasi Payments

Aplikasi `payments` menangani sistem pembayaran pendaftaran, verifikasi, dan manajemen rekening bank.

## 1. BankAccount

Model untuk menyimpan data rekening bank milik pondok (tujuan transfer).

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `nama_bank` | CharField | Pilihan bank (BCA, BNI, BRI, dll). |
| `nama_bank_custom` | CharField | Nama bank manual jika pilih 'Lainnya'. |
| `nomor_rekening` | CharField | Nomor rekening tujuan. |
| `nama_pemilik_rekening` | CharField | Atas nama rekening. |
| `biaya_pendaftaran` | DecimalField | Nominal biaya pendaftaran. |
| `is_active` | BooleanField | Status aktif rekening. |
| `keterangan` | TextField | Catatan tambahan. |
| `order` | PositiveIntegerField | Urutan tampil. |

## 2. Payment

Model untuk menyimpan bukti pembayaran dari santri.

### Fields

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `santri` | OneToOneField | Relasi ke model `Santri`. |
| `bank_pengirim` | CharField | Bank asal transfer. |
| `no_rekening_pengirim` | CharField | No rekening pengirim. |
| `nama_pemilik_rekening` | CharField | Nama pemilik rekening pengirim. |
| `rekening_tujuan` | CharField | Rekening pondok tujuan transfer. |
| `jumlah_transfer` | DecimalField | Jumlah nominal yang ditransfer. |
| `bukti_transfer` | ImageField | Upload foto bukti transfer. |
| `status` | CharField | `pending`, `verified`, `rejected`. |
| `catatan` | TextField | Catatan dari admin (misal alasan tolak). |
| `verified_by` | ForeignKey | User yang memverifikasi. |
| `verified_at` | DateTimeField | Waktu verifikasi. |

### Status

- `pending`: Menunggu Verifikasi.
- `verified`: Pembayaran diterima/valid.
- `rejected`: Pembayaran ditolak/tidak valid.
