# Dokumentasi Endpoints Aplikasi Payments

Base URL: `/payments/`.

## Transaksi Pembayaran

| URL Pattern | View Name | Deskripsi |
|-------------|-----------|-----------|
| `create/<santri_id>/` | `create` | Form upload bukti pembayaran untuk santri tertentu. |
| `detail/<payment_id>/` | `detail` | Halaman detail/status pembayaran. |

## Manajemen Pembayaran (Admin Panel)

Endpoint manajemen pembayaran diakses melalui `admin_panel` (lihat dokumentasi Admin Panel).

- List Pembayaran: `/admin-panel/pembayaran/`
- Verifikasi: `/admin-panel/pembayaran/<id>/verify/`
