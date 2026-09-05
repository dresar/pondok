# PSB Pondok - Panduan Instalasi dan Setup Local

Proyek Django untuk sistem Pendaftaran Santri Baru (PSB) Pondok Pesantren.

## 📋 Persyaratan Sistem

- **Python**: 3.10 atau lebih tinggi
- **XAMPP**: Versi terbaru (untuk MySQL/MariaDB)
- **Git**: (opsional, untuk clone repository)

## 🚀 Langkah-langkah Instalasi

### 1. Install Python

1. Download Python dari [python.org](https://www.python.org/downloads/)
2. Saat instalasi, **centang** opsi "Add Python to PATH"
3. Verifikasi instalasi dengan membuka Command Prompt/PowerShell:
   ```bash
   python --version
   ```

### 2. Install dan Setup XAMPP

1. Download XAMPP dari [apachefriends.org](https://www.apachefriends.org/download.html)
2. Install XAMPP (disarankan di `C:\xampp`)
3. Buka **XAMPP Control Panel**
4. Start **Apache** dan **MySQL**
5. Buka browser dan akses `http://localhost/phpmyadmin`
6. Buat database baru dengan nama `ponpes`:
   - Klik "New" di sidebar kiri
   - Masukkan nama database: `ponpes`
   - Pilih collation: `utf8mb4_general_ci`
   - Klik "Create"

### 3. Setup Virtual Environment

1. Buka Command Prompt/PowerShell di folder proyek:
   ```bash
   cd C:\Users\eka\Downloads\pondok
   ```

2. **Cek versi Python terlebih dahulu:**
   ```bash
   python --version
   ```
   Pastikan Python 3.10 atau lebih tinggi terinstall.

3. Buat virtual environment (jika belum ada atau jika venv lama bermasalah):
   ```bash
   python -m venv venv
   ```
   
   **Jika venv sudah ada tapi bermasalah, hapus dulu:**
   ```powershell
   Remove-Item -Recurse -Force venv
   python -m venv venv
   ```

4. Aktifkan virtual environment:
   
   **Cara 1: Menggunakan Script Helper (Paling Mudah)**
   
   **PowerShell:**
   ```powershell
   .\activate_venv.ps1
   ```
   
   **CMD:**
   ```cmd
   activate_venv.bat
   ```
   
   **Cara 2: Langsung (PowerShell)**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **Jika muncul error "running scripts is disabled":**
   
   **Opsi A - Bypass untuk session ini saja (Recommended):**
   ```powershell
   powershell -ExecutionPolicy Bypass -Command ".\venv\Scripts\Activate.ps1"
   ```
   
   **Opsi B - Set execution policy (permanen untuk user):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Lalu restart PowerShell dan coba lagi.
   
   **Opsi C - Gunakan CMD sebagai alternatif:**
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   **Cara 3: Tanpa Activate (Alternatif)**
   Anda juga bisa menggunakan Python dari venv langsung tanpa activate:
   ```powershell
   .\venv\Scripts\python.exe --version
   .\venv\Scripts\pip.exe install -r requirements.txt
   ```

5. Verifikasi virtual environment aktif:
   ```bash
   python --version
   python -c "import sys; print(sys.executable)"
   ```
   Pastikan path menunjukkan `...\pondok\venv\Scripts\python.exe`

### 4. Install Dependencies

Install semua package yang diperlukan:

```bash
pip install -r requirements.txt
```

**Catatan:** Jika ada error saat install `PyMySQL`, coba install secara terpisah:
```bash
pip install PyMySQL
```

### 5. Konfigurasi Database

Proyek ini sudah dikonfigurasi untuk menggunakan database MySQL di XAMPP dengan setting default:
- **Database Name**: `ponpes`
- **User**: `root`
- **Password**: (kosong)
- **Host**: `localhost`
- **Port**: `3306`

Jika Anda menggunakan konfigurasi berbeda, buat file `.env` di root folder proyek:

```env
DB_NAME=ponpes
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

### 6. Migrate Database

Jalankan migrasi untuk membuat semua tabel database:

```bash
python manage.py migrate
```

Ini akan membuat semua tabel yang diperlukan untuk aplikasi:
- Tabel user dan autentikasi
- Tabel core (website settings, dll)
- Tabel admissions (pendaftaran)
- Tabel blog
- Tabel documents
- Tabel payments
- Tabel admin_panel
- Dan tabel lainnya

### 7. Buat Superuser (Admin)

Buat akun admin untuk mengakses Django Admin Panel:

```bash
python manage.py createsuperuser
```

Ikuti instruksi untuk memasukkan:
- Username
- Email (opsional)
- Password (minimal 8 karakter)

### 8. Generate Data Dummy (Opsional)

#### A. Data Dummy Lengkap (Semua Aplikasi)

Untuk membuat data dummy untuk semua aplikasi:

```bash
python manage.py generate_dummy_data --count 50
```

**Opsi:**
- `--count`: Jumlah data dummy untuk Santri, BlogPost, dll (default: 50)
- `--clear`: Hapus semua data sebelum membuat data baru

**Contoh:**
```bash
# Buat 50 data dummy
python manage.py generate_dummy_data --count 50

# Hapus data lama dan buat 100 data dummy baru
python manage.py generate_dummy_data --count 100 --clear
```

**Data yang dibuat:**
- Akun demo (admin, petugas, bendahara)
- 50 Santri dengan berbagai status
- 25 Blog Posts dengan categories dan tags
- 10 Testimoni
- 5 Pengumuman
- Document Templates
- Bank Accounts dan Payments
- 25 Tenaga Pengajar
- Kontak/Inquiry
- Data Core App (WebsiteSettings, VisiMisi, dll)

**Akun Demo yang dibuat:**
- Username: `admin`, Password: `admin123` (Superadmin)
- Username: `petugas`, Password: `petugas123` (Petugas Pendaftaran)
- Username: `bendahara`, Password: `bendahara123` (Bendahara)

#### B. Data Dummy WhatsApp & Kontak

Untuk membuat data dummy khusus fitur WhatsApp & Kontak:

```bash
python manage.py create_whatsapp_kontak_dummy
```

**Opsi:**
- `--clear`: Hapus semua data WhatsApp & Kontak sebelum membuat data baru

**Contoh:**
```bash
# Buat data dummy WhatsApp & Kontak
python manage.py create_whatsapp_kontak_dummy

# Hapus data lama dan buat data baru
python manage.py create_whatsapp_kontak_dummy --clear
```

**Data yang dibuat:**
- **6 Kategori Template WhatsApp:**
  - Pendaftaran
  - Pembayaran
  - Pengumuman
  - Reminder
  - Selamat Datang
  - Broadcast

- **11 Template WhatsApp:**
  - 4 Template Public (untuk website)
  - 7 Template System (untuk admin panel/broadcast)
  - Template dengan variabel dinamis (nama, tanggal, dll)

- **5 Contact Person:**
  - Panitia pendaftaran dengan nomor WhatsApp

- **30 Kontak/Inquiry:**
  - Inquiry dari website dengan berbagai status
  - Pertanyaan tentang pendaftaran, biaya, fasilitas, dll

### 9. Collect Static Files (Opsional)

Untuk mengumpulkan semua file static:

```bash
python manage.py collectstatic
```

Jawab `yes` jika diminta.

### 10. Menjalankan Server Development

Jalankan server development Django:

```bash
python manage.py runserver
```

Server akan berjalan di `http://127.0.0.1:8000/`

**Catatan:** Pastikan XAMPP MySQL sudah running sebelum menjalankan server!

## 📝 Akses Aplikasi

Setelah server berjalan, Anda dapat mengakses:

- **Homepage**: `http://127.0.0.1:8000/`
- **Admin Panel**: `http://127.0.0.1:8000/admin-panel/`
- **Django Admin**: `http://127.0.0.1:8000/admin/`
- **Login**: `http://127.0.0.1:8000/users/login/`

## 🔧 Troubleshooting

### Error: "mysqlclient 2.2.1 or newer is required; you have 1.4.6"

**Solusi:**
Error ini terjadi karena Django 6.0 memerlukan mysqlclient 2.2.1+, tapi PyMySQL menunjukkan versi yang lebih rendah. Proyek ini sudah dikonfigurasi untuk mengatasi masalah ini melalui `psb_pondok/__init__.py`.

Jika masih muncul error:
1. Pastikan `psb_pondok/__init__.py` sudah ada dan berisi konfigurasi PyMySQL
2. Pastikan `manage.py` mengimport `psb_pondok` sebelum Django setup
3. Restart terminal/PowerShell dan coba lagi
4. Jika masih error, coba:
   ```powershell
   pip uninstall -y PyMySQL
   pip install PyMySQL>=1.1.0
   ```

### Error: "Can't connect to MySQL server"

**Solusi:**
1. Pastikan XAMPP MySQL sudah running di XAMPP Control Panel
2. Pastikan database `ponpes` sudah dibuat di phpMyAdmin
3. Cek koneksi dengan membuka phpMyAdmin di browser
4. Test koneksi dengan script:
   ```powershell
   python test_db_connection.py
   ```

### Error: "No module named 'xxx'"

**Solusi:**
1. Pastikan virtual environment sudah aktif
2. Install ulang dependencies: `pip install -r requirements.txt`

### Error: Venv tidak bisa diaktifkan atau "No Python at '...'"

**Solusi:**
Jika venv tidak bisa diaktifkan atau muncul error tentang Python path yang tidak ditemukan, kemungkinan venv dibuat dengan Python versi/lokasi yang berbeda. Buat ulang venv:

```powershell
# Hapus venv lama
Remove-Item -Recurse -Force venv

# Buat venv baru dengan Python yang aktif
python -m venv venv

# Aktifkan venv
.\venv\Scripts\Activate.ps1

# Verifikasi Python di venv
python --version
```

**Catatan:** Pastikan Python yang digunakan saat membuat venv sama dengan yang akan digunakan untuk menjalankan aplikasi.

### Error: "running scripts is disabled on this system" di PowerShell

**Solusi:**
Ini adalah masalah execution policy PowerShell. Gunakan salah satu solusi berikut:

**Solusi 1: Gunakan Script Helper (Paling Mudah)**
```powershell
.\activate_venv.ps1
```

**Solusi 2: Bypass untuk Session Ini**
```powershell
powershell -ExecutionPolicy Bypass -Command ".\venv\Scripts\Activate.ps1"
```

**Solusi 3: Set Execution Policy (Permanen)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Lalu restart PowerShell.

**Solusi 4: Gunakan CMD sebagai Alternatif**
Buka Command Prompt (CMD) dan jalankan:
```cmd
cd C:\Users\eka\Downloads\pondok
activate_venv.bat
```

**Solusi 5: Gunakan Python Langsung Tanpa Activate**
```powershell
.\venv\Scripts\python.exe manage.py runserver
.\venv\Scripts\pip.exe install -r requirements.txt
```

### Error: "Access denied for user 'root'@'localhost'"

**Solusi:**
1. Buka phpMyAdmin
2. Klik "User accounts" → "root" → "Edit privileges"
3. Pastikan password kosong atau sesuaikan di file `.env`

### Error saat migrate: "Table already exists"

**Solusi:**
Jika tabel sudah ada, Anda bisa:
1. Hapus database dan buat ulang di phpMyAdmin
2. Atau gunakan `python manage.py migrate --run-syncdb`

### Port 8000 sudah digunakan

**Solusi:**
Jalankan server di port lain:
```bash
python manage.py runserver 8080
```

## 📦 Struktur Proyek

```
pondok/
├── admin_panel/      # Panel admin untuk manajemen
├── admissions/       # Modul pendaftaran santri
├── blog/            # Modul blog/artikel
├── core/            # Core settings dan utilities
├── documents/       # Modul dokumen
├── payments/        # Modul pembayaran
├── users/           # Modul user dan autentikasi
├── templates/       # Template HTML
├── static/          # File static (CSS, JS, images)
├── media/           # File upload (user uploads)
├── logs/            # Log files
├── manage.py        # Django management script
└── requirements.txt # Dependencies
```

## 🔐 Default Settings

- **Debug Mode**: `True` (untuk development)
- **Database**: MySQL/MariaDB via XAMPP
- **Timezone**: `Asia/Jakarta`
- **Language**: `id-id` (Bahasa Indonesia)

## 📚 Command yang Sering Digunakan

```bash
# Aktifkan virtual environment (Pilih salah satu)
.\activate_venv.ps1          # Menggunakan script helper (PowerShell)
activate_venv.bat             # Menggunakan script helper (CMD)
.\venv\Scripts\Activate.ps1   # Langsung (PowerShell)
venv\Scripts\activate.bat     # Langsung (CMD)

# Install dependencies
pip install -r requirements.txt

# Migrate database
python manage.py migrate

# Buat superuser
python manage.py createsuperuser

# Generate data dummy
python manage.py generate_dummy_data --count 50
python manage.py generate_dummy_data --count 100 --clear  # Hapus data lama dulu

# Generate data dummy WhatsApp & Kontak
python manage.py create_whatsapp_kontak_dummy
python manage.py create_whatsapp_kontak_dummy --clear  # Hapus data lama dulu

# Jalankan server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Buat migration baru (setelah edit models)
python manage.py makemigrations

# Django shell
python manage.py shell

# Test koneksi database
python test_db_connection.py
```

## ⚠️ Catatan Penting

1. **Jangan commit file `.env`** ke repository (jika menggunakan)
2. **Jangan commit folder `venv/`** ke repository
3. **Backup database** secara berkala
4. **Gunakan environment variables** untuk production
5. Pastikan **XAMPP MySQL running** sebelum menjalankan aplikasi

## 🆘 Bantuan

Jika mengalami masalah:
1. Cek log di folder `logs/`
2. Pastikan semua persyaratan sudah terinstall
3. Pastikan XAMPP MySQL sudah running
4. Cek konfigurasi database di `psb_pondok/settings.py`

---

**Selamat coding! 🎉**

