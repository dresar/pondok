"""
Management command untuk membuat data dummy BagianJabatan dan TenagaPengajar

Usage:
    python manage.py create_dummy_tenaga_pengajar --count 20
    python manage.py create_dummy_tenaga_pengajar --count 50 --clear

Options:
    --count: Jumlah tenaga pengajar yang akan dibuat (default: 20)
    --clear: Hapus semua data BagianJabatan dan TenagaPengajar sebelum membuat data baru

Contoh:
    # Membuat 25 tenaga pengajar
    python manage.py create_dummy_tenaga_pengajar --count 25
    
    # Hapus semua data lama dan buat 30 tenaga pengajar baru
    python manage.py create_dummy_tenaga_pengajar --count 30 --clear
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from core.models import BagianJabatan, TenagaPengajar


class Command(BaseCommand):
    help = 'Membuat data dummy BagianJabatan dan TenagaPengajar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Jumlah tenaga pengajar yang akan dibuat (default: 20)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus semua data BagianJabatan dan TenagaPengajar sebelum membuat data baru'
        )

    def handle(self, *args, **options):
        count = options['count']
        clear = options['clear']
        
        if clear:
            self.stdout.write(self.style.WARNING('Menghapus data lama...'))
            TenagaPengajar.objects.all().delete()
            BagianJabatan.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data lama berhasil dihapus.'))
        
        # Buat Bagian/Jabatan
        self.stdout.write(self.style.SUCCESS('Membuat Bagian/Jabatan...'))
        bagian_data = [
            {'nama': 'Pendiri', 'deskripsi': 'Pendiri pesantren', 'order': 1},
            {'nama': 'Pimpinan', 'deskripsi': 'Pimpinan pesantren', 'order': 2},
            {'nama': 'Kepala Sekolah', 'deskripsi': 'Kepala sekolah pesantren', 'order': 3},
            {'nama': 'Wakil Kepala Sekolah', 'deskripsi': 'Wakil kepala sekolah', 'order': 4},
            {'nama': 'Ustadz Senior', 'deskripsi': 'Ustadz senior dengan pengalaman mengajar lama', 'order': 5},
            {'nama': 'Ustadzah Senior', 'deskripsi': 'Ustadzah senior dengan pengalaman mengajar lama', 'order': 6},
            {'nama': 'Ustadz', 'deskripsi': 'Tenaga pengajar laki-laki', 'order': 7},
            {'nama': 'Ustadzah', 'deskripsi': 'Tenaga pengajar perempuan', 'order': 8},
            {'nama': 'Guru Agama', 'deskripsi': 'Guru mata pelajaran agama', 'order': 9},
            {'nama': 'Guru Umum', 'deskripsi': 'Guru mata pelajaran umum', 'order': 10},
        ]
        
        bagian_objects = {}
        for data in bagian_data:
            bagian, created = BagianJabatan.objects.get_or_create(
                nama=data['nama'],
                defaults={
                    'deskripsi': data['deskripsi'],
                    'order': data['order'],
                    'is_active': True
                }
            )
            bagian_objects[data['nama']] = bagian
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Bagian "{data["nama"]}" dibuat'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Bagian "{data["nama"]}" sudah ada'))
        
        # Data dummy untuk nama
        nama_depan_laki = [
            'Ahmad', 'Muhammad', 'Ali', 'Hasan', 'Husain', 'Umar', 'Usman', 'Abdullah',
            'Abdurrahman', 'Ibrahim', 'Ismail', 'Yusuf', 'Yunus', 'Rahmat', 'Rizki',
            'Fadil', 'Fauzan', 'Maulana', 'Hidayat', 'Fauzi', 'Pratama', 'Kurniawan',
            'Wibowo', 'Santoso', 'Siregar', 'Nasution', 'Lubis', 'Harahap'
        ]
        
        nama_depan_perempuan = [
            'Fatimah', 'Aisyah', 'Khadijah', 'Zainab', 'Mariam', 'Nur', 'Siti',
            'Dinda', 'Putri', 'Sari', 'Indah', 'Rina', 'Lina', 'Dewi', 'Sinta',
            'Rahma', 'Nabila', 'Aulia', 'Fadila', 'Khadijah', 'Maryam', 'Hafizah'
        ]
        
        nama_belakang = [
            'Rahman', 'Hakim', 'Nur', 'Sari', 'Hidayat', 'Maulana', 'Fauzi', 'Rizki',
            'Pratama', 'Kurniawan', 'Wibowo', 'Santoso', 'Siregar', 'Nasution', 'Lubis',
            'Harahap', 'Dalimunthe', 'Tanjung', 'Pohan', 'Ginting', 'Sembiring', 'Sinaga'
        ]
        
        tempat_lahir = [
            'Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Palembang', 'Pekanbaru', 'Padang',
            'Jambi', 'Bengkulu', 'Lampung', 'Banten', 'Yogyakarta', 'Semarang', 'Malang',
            'Solo', 'Makassar', 'Denpasar', 'Pontianak', 'Balikpapan', 'Samarinda'
        ]
        
        universitas = [
            'Universitas Al-Azhar Kairo', 'Universitas Islam Negeri Jakarta', 
            'Universitas Islam Negeri Yogyakarta', 'Universitas Islam Negeri Bandung',
            'Universitas Islam Negeri Surabaya', 'Universitas Islam Negeri Medan',
            'Pondok Modern Darussalam Gontor', 'Pondok Modern Darussalam Mantingan',
            'Universitas Muhammadiyah Jakarta', 'Universitas Muhammadiyah Yogyakarta',
            'Institut Agama Islam Negeri', 'Universitas Islam Indonesia',
            'Universitas Gadjah Mada', 'Universitas Indonesia', 'Institut Teknologi Bandung'
        ]
        
        bidang_keahlian = [
            'Tafsir Al-Qur\'an', 'Hadits', 'Fiqih', 'Aqidah', 'Bahasa Arab', 'Nahwu Shorof',
            'Tajwid', 'Sejarah Islam', 'Matematika', 'Fisika', 'Kimia', 'Biologi',
            'Bahasa Indonesia', 'Bahasa Inggris', 'Ekonomi', 'Sejarah', 'Geografi',
            'Sosiologi', 'Psikologi', 'Pendidikan Agama Islam'
        ]
        
        mata_pelajaran_list = [
            'Tafsir Al-Qur\'an, Hadits, Fiqih',
            'Bahasa Arab, Nahwu, Shorof',
            'Tajwid, Tahfidz Al-Qur\'an',
            'Aqidah, Akhlak, Sejarah Islam',
            'Matematika, Fisika, Kimia',
            'Bahasa Indonesia, Bahasa Inggris',
            'Ekonomi, Sejarah, Geografi',
            'Pendidikan Agama Islam, Fiqih',
            'Bahasa Arab, Tafsir, Hadits',
            'Matematika, IPA, IPS'
        ]
        
        motto_list = [
            'Menuntut ilmu adalah ibadah',
            'Ilmu tanpa amal bagaikan pohon tanpa buah',
            'Bersungguh-sungguhlah dalam menuntut ilmu',
            'Pendidikan adalah investasi terbaik',
            'Mengajar adalah amal jariyah',
            'Ilmu yang bermanfaat adalah ilmu yang diamalkan',
            'Belajar sepanjang hayat',
            'Pendidikan membentuk karakter',
            'Ilmu adalah cahaya kehidupan',
            'Mengajar dengan hati'
        ]
        
        # Buat Tenaga Pengajar
        self.stdout.write(self.style.SUCCESS(f'\nMembuat {count} Tenaga Pengajar...'))
        
        created_count = 0
        for i in range(count):
            # Tentukan jenis kelamin (50% laki-laki, 50% perempuan)
            jenis_kelamin = random.choice(['L', 'P'])
            
            # Pilih nama sesuai jenis kelamin
            if jenis_kelamin == 'L':
                nama_depan = random.choice(nama_depan_laki)
                bagian_jabatan = random.choice([
                    bagian_objects['Pendiri'],
                    bagian_objects['Pimpinan'],
                    bagian_objects['Kepala Sekolah'],
                    bagian_objects['Wakil Kepala Sekolah'],
                    bagian_objects['Ustadz Senior'],
                    bagian_objects['Ustadz'],
                    bagian_objects['Guru Agama'],
                    bagian_objects['Guru Umum'],
                ])
            else:
                nama_depan = random.choice(nama_depan_perempuan)
                bagian_jabatan = random.choice([
                    bagian_objects['Pimpinan'],
                    bagian_objects['Kepala Sekolah'],
                    bagian_objects['Wakil Kepala Sekolah'],
                    bagian_objects['Ustadzah Senior'],
                    bagian_objects['Ustadzah'],
                    bagian_objects['Guru Agama'],
                    bagian_objects['Guru Umum'],
                ])
            
            nama_belakang = random.choice(nama_belakang)
            nama_lengkap = f"{nama_depan} {nama_belakang}"
            nama_panggilan = nama_depan
            
            # Generate tanggal lahir (usia 25-60 tahun)
            tahun_lahir = random.randint(1965, 2000)
            bulan_lahir = random.randint(1, 12)
            hari_lahir = random.randint(1, 28)
            tanggal_lahir = datetime(tahun_lahir, bulan_lahir, hari_lahir).date()
            
            # Generate tahun lulus (setelah tahun lahir + 20)
            tahun_lulus = str(random.randint(tahun_lahir + 20, tahun_lahir + 25))
            
            # Buat tenaga pengajar
            pengajar = TenagaPengajar.objects.create(
                nama_lengkap=nama_lengkap,
                nama_panggilan=nama_panggilan,
                jenis_kelamin=jenis_kelamin,
                bagian_jabatan=bagian_jabatan,
                tempat_lahir=random.choice(tempat_lahir),
                tanggal_lahir=tanggal_lahir,
                alamat=f"Jl. {random.choice(['Merdeka', 'Sudirman', 'Gatot Subroto', 'Ahmad Yani', 'Diponegoro'])} No. {random.randint(1, 999)}, {random.choice(tempat_lahir)}",
                no_hp=f"08{random.randint(100000000, 999999999)}",
                email=f"{nama_depan.lower()}.{nama_belakang.lower()}@pondok.id",
                pendidikan_terakhir=random.choice(['S1 Pendidikan Agama Islam', 'S1 Tafsir Al-Qur\'an', 'S1 Hadits', 'S1 Fiqih', 'S1 Bahasa Arab', 'S2 Pendidikan Islam', 'S2 Tafsir', 'S1 Matematika', 'S1 Fisika', 'S1 Kimia']),
                universitas=random.choice(universitas),
                tahun_lulus=tahun_lulus,
                bidang_keahlian=random.choice(bidang_keahlian),
                mata_pelajaran=random.choice(mata_pelajaran_list),
                pengalaman_mengajar=f"Pengalaman mengajar selama {random.randint(5, 30)} tahun di berbagai pesantren dan sekolah. Mengajar mata pelajaran {random.choice(bidang_keahlian)} dengan dedikasi tinggi.",
                prestasi=f"Prestasi: {'Juara 1' if random.choice([True, False]) else 'Juara 2'} {'Lomba Tahfidz' if random.choice([True, False]) else 'Lomba Pidato'} {'Nasional' if random.choice([True, False]) else 'Regional'} tahun {random.randint(2010, 2024)}",
                riwayat_pendidikan=f"SD: SD Islam {random.choice(['Al-Azhar', 'Nurul Iman', 'Al-Ikhlas'])} ({tahun_lahir + 6}-{tahun_lahir + 12})\nSMP: SMP Islam {random.choice(['Al-Azhar', 'Nurul Iman', 'Al-Ikhlas'])} ({tahun_lahir + 12}-{tahun_lahir + 15})\nSMA: SMA Islam {random.choice(['Al-Azhar', 'Nurul Iman', 'Al-Ikhlas'])} ({tahun_lahir + 15}-{tahun_lahir + 18})\nS1: {random.choice(universitas)} ({tahun_lahir + 18}-{tahun_lahir + 22})",
                organisasi=f"Anggota {'IKADI' if random.choice([True, False]) else 'MUI'} {'Kabupaten' if random.choice([True, False]) else 'Kota'} {random.choice(tempat_lahir)}",
                karya_tulis=f"Penulis buku '{random.choice(['Panduan Tahfidz', 'Metode Belajar Bahasa Arab', 'Fiqih Praktis', 'Tafsir Juz Amma'])}' tahun {random.randint(2015, 2024)}",
                motto=random.choice(motto_list),
                # Media Sosial (70% chance memiliki media sosial)
                whatsapp=f"62{random.randint(800, 899)}{random.randint(10000000, 99999999)}" if random.choice([True, True, True, False]) else '',
                facebook=f"https://facebook.com/{nama_depan.lower()}.{nama_belakang.lower()}" if random.choice([True, True, False]) else '',
                instagram=f"https://instagram.com/{nama_depan.lower()}_{nama_belakang.lower()}" if random.choice([True, True, False]) else '',
                twitter=f"https://twitter.com/{nama_depan.lower()}_{nama_belakang.lower()}" if random.choice([True, False, False]) else '',
                linkedin=f"https://linkedin.com/in/{nama_depan.lower()}-{nama_belakang.lower()}" if random.choice([True, False, False]) else '',
                youtube=f"https://youtube.com/@{nama_depan.lower()}{nama_belakang.lower()}" if random.choice([True, False, False, False]) else '',
                tiktok=f"https://tiktok.com/@{nama_depan.lower()}_{nama_belakang.lower()}" if random.choice([True, False, False, False]) else '',
                order=i + 1,
                is_published=random.choice([True, True, True, False]),  # 75% published
                is_featured=random.choice([True, False, False, False]) if i < 10 else False,  # 10 pertama bisa featured
            )
            
            created_count += 1
            if created_count % 5 == 0:
                self.stdout.write(f'  [OK] {created_count}/{count} pengajar dibuat...')
        
        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Berhasil membuat {created_count} tenaga pengajar!'))
        self.stdout.write(self.style.SUCCESS(f'[INFO] Total Bagian/Jabatan: {BagianJabatan.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'[INFO] Total Tenaga Pengajar: {TenagaPengajar.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'[INFO] Featured Pengajar: {TenagaPengajar.objects.filter(is_featured=True).count()}'))

