"""
Management command untuk reset dan membuat data dummy santri lengkap dengan semua formulir dan dokumen
Usage: python manage.py create_dummy_santri --count 100
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
import random
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
from admissions.models import Santri
from payments.models import Payment
from users.models import User
from decimal import Decimal


class Command(BaseCommand):
    help = 'Reset dan membuat data dummy santri lengkap dengan semua formulir dan dokumen'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Jumlah santri yang akan dibuat (default: 100)'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset semua data santri yang sudah ada sebelum membuat data baru'
        )

    def generate_dummy_image(self, text, width=800, height=600, bg_color=(240, 240, 240), text_color=(100, 100, 100)):
        """Generate dummy image dengan text"""
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default if not available
        try:
            # Try to use arial font
            font_size = 40
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 40)
            except:
                font = ImageFont.load_default()
        
        # Calculate text position (center)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2)
        
        draw.text(position, text, fill=text_color, font=font)
        
        # Save to BytesIO
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        return ContentFile(img_io.read())

    def handle(self, *args, **options):
        count = options['count']
        reset = options.get('reset', True)  # Default reset
        
        # Reset data jika diminta
        if reset:
            self.stdout.write(self.style.WARNING('Menghapus semua data santri yang sudah ada...'))
            deleted_count = Santri.objects.all().delete()[0]
            self.stdout.write(self.style.SUCCESS(f'Berhasil menghapus {deleted_count} data santri'))
        
        # Data dummy
        nama_depan_laki = [
            'Ahmad', 'Muhammad', 'Ali', 'Hasan', 'Husain', 'Umar', 'Usman', 'Abdullah',
            'Abdurrahman', 'Ibrahim', 'Ismail', 'Yusuf', 'Yunus', 'Rahmat', 'Rizki', 'Fadil',
            'Fauzan', 'Hafiz', 'Hamzah', 'Haris', 'Ihsan', 'Iqbal', 'Jalal', 'Khalid',
            'Luthfi', 'Mahmud', 'Nabil', 'Omar', 'Qasim', 'Rafi', 'Salman', 'Taufik',
            'Ubaid', 'Wahid', 'Yasin', 'Zaid', 'Zaki', 'Zulfikar', 'Amir', 'Bilal',
            'Dani', 'Eko', 'Faris', 'Gani', 'Hadi', 'Ilyas', 'Jamil', 'Kamil', 'Lukman', 'Mansur'
        ]
        
        nama_depan_perempuan = [
            'Fatimah', 'Aisyah', 'Khadijah', 'Zainab', 'Mariam', 'Nur', 'Siti', 'Dinda',
            'Putri', 'Sari', 'Indah', 'Rina', 'Lina', 'Dewi', 'Sinta', 'Ayu', 'Bunga',
            'Cinta', 'Dewi', 'Eka', 'Fira', 'Gita', 'Hani', 'Ika', 'Jihan', 'Kartika',
            'Laila', 'Maya', 'Nadia', 'Oktavia', 'Putri', 'Qonita', 'Rahma', 'Salsabila',
            'Tasya', 'Umi', 'Vina', 'Winda', 'Yuli', 'Zahra', 'Alya', 'Bella', 'Citra',
            'Dara', 'Elsa', 'Fadila', 'Gina', 'Hilda', 'Ira', 'Jihan', 'Kiki'
        ]
        
        nama_belakang = [
            'Rahman', 'Hakim', 'Nur', 'Sari', 'Putra', 'Putri', 'Wati', 'Hidayat',
            'Maulana', 'Fauzi', 'Rizki', 'Pratama', 'Kurniawan', 'Wibowo', 'Santoso',
            'Siregar', 'Nasution', 'Lubis', 'Harahap', 'Dalimunthe', 'Tanjung', 'Pohan',
            'Saputra', 'Wijaya', 'Suryadi', 'Purnomo', 'Setiawan', 'Kusuma', 'Wardhana',
            'Pramono', 'Sutrisno', 'Wibisono', 'Sukarno', 'Harto', 'Susilo', 'Bambang',
            'Eko', 'Joko', 'Budi', 'Agung', 'Arief', 'Darmawan', 'Gunawan', 'Handoko'
        ]
        
        tempat_lahir = [
            'Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Palembang', 'Pekanbaru', 'Padang', 'Jambi',
            'Bengkulu', 'Lampung', 'Banten', 'Yogyakarta', 'Semarang', 'Malang', 'Solo', 'Makassar',
            'Denpasar', 'Pontianak', 'Balikpapan', 'Samarinda', 'Manado', 'Palu', 'Kendari', 'Ambon',
            'Bogor', 'Depok', 'Tangerang', 'Bekasi', 'Cirebon', 'Tasikmalaya', 'Purwokerto', 'Magelang'
        ]
        
        pekerjaan = [
            'PNS', 'Guru', 'Dosen', 'Dokter', 'Perawat', 'Wiraswasta', 'Pedagang', 'Petani',
            'Nelayan', 'Karyawan Swasta', 'Pegawai Bank', 'Polisi', 'TNI', 'Pensiunan', 'Ibu Rumah Tangga',
            'Pengusaha', 'Konsultan', 'Arsitek', 'Insinyur', 'Akuntan', 'Notaris', 'Hakim', 'Jaksa'
        ]
        
        pendidikan = [
            'SD SEDERAJAT', 'SMP SEDERAJAT', 'SMA SEDERAJAT', 'D3', 'S1', 'S2', 'S3'
        ]
        
        sekolah = [
            'SD Negeri 01', 'SD Negeri 02', 'SD Islam Terpadu', 'MI Al-Hidayah', 'MI Nurul Iman',
            'SMP Negeri 01', 'SMP Negeri 02', 'MTs Al-Azhar', 'MTs Darussalam', 'MTs Al-Ikhlas',
            'SMA Negeri 01', 'SMA Negeri 02', 'MA Al-Amin', 'MA Darul Ulum', 'MA Al-Muttaqin',
            'SD Muhammadiyah', 'SMP Muhammadiyah', 'SMA Muhammadiyah', 'MA Muhammadiyah'
        ]
        
        kelas = ['6 SD', '9 SMP', '12 SMA', '12 MA']
        
        provinsi_list = [
            'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Sumatera Utara',
            'Sumatera Selatan', 'Riau', 'Sumatera Barat', 'Jambi', 'Bengkulu', 'Lampung',
            'Banten', 'DI Yogyakarta', 'Kalimantan Barat', 'Kalimantan Tengah', 'Kalimantan Selatan',
            'Kalimantan Timur', 'Sulawesi Selatan', 'Sulawesi Utara', 'Bali', 'Nusa Tenggara Barat'
        ]
        
        kabupaten_list = [
            'Jakarta Selatan', 'Jakarta Utara', 'Jakarta Timur', 'Jakarta Barat', 'Jakarta Pusat',
            'Bandung', 'Bogor', 'Depok', 'Tangerang', 'Bekasi', 'Surabaya', 'Malang', 'Semarang',
            'Yogyakarta', 'Medan', 'Palembang', 'Pekanbaru', 'Padang', 'Makassar', 'Denpasar'
        ]
        
        kecamatan_list = [
            'Kecamatan A', 'Kecamatan B', 'Kecamatan C', 'Kecamatan D', 'Kecamatan E',
            'Kecamatan F', 'Kecamatan G', 'Kecamatan H', 'Kecamatan I', 'Kecamatan J'
        ]
        
        desa_list = [
            'Desa A', 'Desa B', 'Desa C', 'Desa D', 'Desa E',
            'Kelurahan A', 'Kelurahan B', 'Kelurahan C', 'Kelurahan D', 'Kelurahan E'
        ]
        
        golongan_darah_list = ['A', 'B', 'AB', 'O']
        
        # Get admin user untuk verified_by
        admin_user = User.objects.filter(is_staff=True).first()
        
        self.stdout.write(f'Membuat {count} data dummy santri dengan formulir lengkap...')
        
        # Pastikan 50% laki-laki, 50% perempuan
        jenis_kelamin_list = (['L'] * (count // 2)) + (['P'] * (count - count // 2))
        random.shuffle(jenis_kelamin_list)
        
        created = 0
        for i in range(count):
            # Generate NISN unik
            nisn = f"{random.randint(1000000000, 9999999999)}"
            while Santri.objects.filter(nisn=nisn).exists():
                nisn = f"{random.randint(1000000000, 9999999999)}"
            
            # Generate jenis kelamin (50-50)
            jenis_kelamin = jenis_kelamin_list[i]
            
            # Generate nama berdasarkan jenis kelamin
            if jenis_kelamin == 'L':
                nama = f"{random.choice(nama_depan_laki)} {random.choice(nama_belakang)}"
            else:
                nama = f"{random.choice(nama_depan_perempuan)} {random.choice(nama_belakang)}"
            
            nama_panggilan = nama.split()[0]
            
            # Generate tanggal lahir (usia 10-18 tahun)
            tahun_lahir = random.randint(2007, 2015)
            bulan = random.randint(1, 12)
            hari = random.randint(1, 28)
            tanggal_lahir = datetime(tahun_lahir, bulan, hari).date()
            
            # Generate data orang tua
            nama_ayah = f"{random.choice(nama_depan_laki)} {random.choice(nama_belakang)}"
            nama_ibu = f"{random.choice(nama_depan_perempuan)} {random.choice(nama_belakang)}"
            
            # Generate NIK (16 digit)
            nik_ayah = f"{random.randint(1000000000000000, 9999999999999999)}"
            nik_ibu = f"{random.randint(1000000000000000, 9999999999999999)}"
            
            # Generate tanggal lahir orang tua (usia 35-55 tahun)
            tahun_lahir_ayah = tahun_lahir - random.randint(20, 40)
            bulan_ayah = random.randint(1, 12)
            hari_ayah = random.randint(1, 28)
            tanggal_lahir_ayah = datetime(tahun_lahir_ayah, bulan_ayah, hari_ayah).date()
            
            tahun_lahir_ibu = tahun_lahir - random.randint(18, 38)
            bulan_ibu = random.randint(1, 12)
            hari_ibu = random.randint(1, 28)
            tanggal_lahir_ibu = datetime(tahun_lahir_ibu, bulan_ibu, hari_ibu).date()
            
            # Generate no HP
            no_hp = f"08{random.randint(100000000, 999999999)}"
            no_hp_ayah = f"08{random.randint(100000000, 999999999)}"
            no_hp_ibu = f"08{random.randint(100000000, 999999999)}"
            
            # Generate email
            email = f"{nama.lower().replace(' ', '')}{i}@gmail.com"
            
            # Generate alamat lengkap
            provinsi = random.choice(provinsi_list)
            kabupaten = random.choice(kabupaten_list)
            kecamatan = random.choice(kecamatan_list)
            desa = random.choice(desa_list)
            jalan = random.choice(['Jl. Merdeka', 'Jl. Sudirman', 'Jl. Gatot Subroto', 'Jl. Ahmad Yani', 'Jl. Diponegoro', 'Jl. Thamrin', 'Jl. Hayam Wuruk'])
            no_rumah = random.randint(1, 999)
            rt = random.randint(1, 10)
            rw = random.randint(1, 10)
            alamat = f"{jalan} No. {no_rumah}, RT {rt:02d}/RW {rw:02d}, {desa}, {kecamatan}, {kabupaten}, {provinsi}"
            kode_pos = f"{random.randint(10000, 99999)}"
            
            # Generate data sekolah
            asal_sekolah = random.choice(sekolah)
            npsn_sekolah = f"{random.randint(10000000, 99999999)}"
            kelas_terakhir = random.choice(kelas)
            tahun_lulus = str(random.randint(2020, 2024))
            no_ijazah = f"DN-{random.randint(100000, 999999)}/{tahun_lulus}"
            
            # Generate data fisik
            golongan_darah = random.choice(golongan_darah_list)
            tinggi_badan = random.randint(140, 180) if jenis_kelamin == 'L' else random.randint(130, 170)
            berat_badan = random.randint(35, 80) if jenis_kelamin == 'L' else random.randint(30, 70)
            anak_ke = random.randint(1, 5)
            jumlah_saudara = random.randint(0, 6)
            
            # Generate dokumen dummy
            foto_santri_file = self.generate_dummy_image(
                f'Foto Santri\n{nama}\nNISN: {nisn}',
                width=400, height=500,
                bg_color=(200, 220, 240), text_color=(50, 50, 50)
            )
            
            foto_ktp_file = self.generate_dummy_image(
                f'Foto KTP/Kartu Keluarga\n{nama_ayah}',
                width=800, height=500,
                bg_color=(250, 250, 200), text_color=(50, 50, 50)
            )
            
            foto_akta_file = self.generate_dummy_image(
                f'Akta Kelahiran\n{nama}\nTempat: {random.choice(tempat_lahir)}\nTanggal: {tanggal_lahir.strftime("%d-%m-%Y")}',
                width=800, height=600,
                bg_color=(240, 250, 240), text_color=(50, 50, 50)
            )
            
            foto_ijazah_file = self.generate_dummy_image(
                f'Ijazah/SKHUN\n{nama}\nAsal: {asal_sekolah}\nNo: {no_ijazah}',
                width=800, height=600,
                bg_color=(250, 240, 250), text_color=(50, 50, 50)
            )
            
            surat_sehat_file = self.generate_dummy_image(
                f'Surat Keterangan Sehat\n{nama}\nTanggal: {datetime.now().strftime("%d-%m-%Y")}',
                width=800, height=600,
                bg_color=(240, 250, 250), text_color=(50, 50, 50)
            )
            
            # Create Santri dengan semua field terisi (tanpa dokumen dulu)
            santri = Santri.objects.create(
                # Data Pribadi
                nama_lengkap=nama,
                nama_panggilan=nama_panggilan,
                nisn=nisn,
                tempat_lahir=random.choice(tempat_lahir),
                tanggal_lahir=tanggal_lahir,
                jenis_kelamin=jenis_kelamin,
                agama='Islam',
                kewarganegaraan='WNI',
                anak_ke=anak_ke,
                jumlah_saudara=jumlah_saudara,
                bahasa_sehari_hari='Indonesia',
                golongan_darah=golongan_darah,
                tinggi_badan=tinggi_badan,
                berat_badan=berat_badan,
                riwayat_penyakit='Tidak ada' if random.random() > 0.1 else random.choice(['Asma ringan', 'Alergi debu', '']),
                tinggal_dengan=random.choice(['Orang Tua', 'Wali', 'Lainnya']),
                
                # Data Ayah
                nama_ayah=nama_ayah,
                nik_ayah=nik_ayah,
                tempat_lahir_ayah=random.choice(tempat_lahir),
                tanggal_lahir_ayah=tanggal_lahir_ayah,
                agama_ayah='Islam',
                kewarganegaraan_ayah='WNI',
                pendidikan_ayah=random.choice(pendidikan),
                pekerjaan_ayah=random.choice(pekerjaan),
                no_hp_ayah=no_hp_ayah,
                status_ayah='HIDUP',
                
                # Data Ibu
                nama_ibu=nama_ibu,
                nik_ibu=nik_ibu,
                tempat_lahir_ibu=random.choice(tempat_lahir),
                tanggal_lahir_ibu=tanggal_lahir_ibu,
                agama_ibu='Islam',
                kewarganegaraan_ibu='WNI',
                pendidikan_ibu=random.choice(pendidikan),
                pekerjaan_ibu=random.choice(pekerjaan),
                no_hp_ibu=no_hp_ibu,
                status_ibu='HIDUP',
                alamat_orangtua=alamat,
                
                # Kontak & Alamat
                alamat=alamat,
                desa=desa,
                kecamatan=kecamatan,
                kabupaten=kabupaten,
                provinsi=provinsi,
                kode_pos=kode_pos,
                no_hp=no_hp,
                email=email,
                
                # Data Sekolah
                asal_sekolah=asal_sekolah,
                npsn_sekolah=npsn_sekolah,
                kelas_terakhir=kelas_terakhir,
                tahun_lulus=tahun_lulus,
                no_ijazah=no_ijazah,
                
                # Status Approval Dokumen (semua disetujui)
                foto_santri_approved=True,
                foto_ktp_approved=True,
                foto_akta_approved=True,
                foto_ijazah_approved=True,
                surat_sehat_approved=True,
                
                # Status
                status='pending',
                catatan='Data dummy untuk testing',
                created_at=timezone.now() - timedelta(days=random.randint(1, 90))
            )
            
            # Simpan dokumen setelah object dibuat
            santri.foto_santri.save(f'{nisn}_foto_santri.jpg', foto_santri_file, save=False)
            santri.foto_ktp.save(f'{nisn}_foto_ktp.jpg', foto_ktp_file, save=False)
            santri.foto_akta.save(f'{nisn}_foto_akta.jpg', foto_akta_file, save=False)
            santri.foto_ijazah.save(f'{nisn}_foto_ijazah.jpg', foto_ijazah_file, save=False)
            santri.surat_sehat.save(f'{nisn}_surat_sehat.jpg', surat_sehat_file, save=False)
            santri.save()  # Save sekali di akhir
            
            created += 1
            if created % 10 == 0:
                self.stdout.write(f'  Created {created}/{count}...')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nBerhasil membuat {created} data dummy santri dengan formulir lengkap dan dokumen!'
            )
        )
        
        # Summary
        total = Santri.objects.count()
        laki_laki = Santri.objects.filter(jenis_kelamin='L').count()
        perempuan = Santri.objects.filter(jenis_kelamin='P').count()
        pending = Santri.objects.filter(status='pending').count()
        verified = Santri.objects.filter(status='verified').count()
        accepted = Santri.objects.filter(status='accepted').count()
        
        self.stdout.write('\n=== SUMMARY ===')
        self.stdout.write(f'Total Santri: {total}')
        self.stdout.write(f'Santri Laki-laki: {laki_laki}')
        self.stdout.write(f'Santri Perempuan: {perempuan}')
        self.stdout.write(f'\nStatus:')
        self.stdout.write(f'  Pending: {pending}')
        self.stdout.write(f'  Verified: {verified}')
        self.stdout.write(f'  Accepted: {accepted}')
        self.stdout.write(f'\nSemua santri memiliki:')
        self.stdout.write(f'  ✓ Formulir lengkap (semua field terisi)')
        self.stdout.write(f'  ✓ Dokumen lengkap (foto_santri, foto_ktp, foto_akta, foto_ijazah, surat_sehat)')
