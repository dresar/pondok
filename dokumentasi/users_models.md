# Dokumentasi Models Aplikasi Users

Aplikasi `users` menangani autentikasi, manajemen user (role), dan log aktivitas login.

## 1. User (Custom User Model)

Meng-extend `AbstractUser` Django.

### Roles

User memiliki field `role` dengan pilihan:
- `superadmin`: Akses penuh sistem.
- `bendahara`: Akses menu keuangan/pembayaran.
- `petugaspendaftaran`: Akses menu pendaftaran santri.
- `user`: User biasa (Wali Santri/Pendaftar).

### Fields Tambahan

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `phone` | CharField | Nomor HP User. |
| `avatar` | ImageField | Foto profil user. |

### Methods

- `is_admin_user()`: Cek apakah superadmin/superuser.
- `is_bendahara()`: Cek apakah role bendahara atau admin.
- `is_petugas_pendaftaran()`: Cek apakah role petugas atau admin.

## 2. LoginHistory

Mencatat riwayat login user untuk audit keamanan.

| Nama Field | Tipe Data | Keterangan |
|------------|-----------|------------|
| `username` | CharField | Username yang mencoba login. |
| `ip_address` | GenericIPAddress | Alamat IP pengguna. |
| `user_agent` | TextField | Info browser/device. |
| `status` | CharField | `success` atau `failed`. |
| `user` | ForeignKey | Relasi ke User (jika login berhasil). |
| `error_message` | CharField | Pesan error jika gagal. |
| `created_at` | DateTimeField | Waktu kejadian. |
