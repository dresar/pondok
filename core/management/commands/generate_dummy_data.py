"""
Management command untuk membuat semua data dummy untuk semua aplikasi
Usage: python manage.py generate_dummy_data [--count=50] [--clear]
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random

from core.models import (
    WebsiteSettings, HeroSection, SejarahTimeline, VisiMisi, ProgramPendidikan,
    Fasilitas, Ekstrakurikuler, JadwalHarian, Persyaratan, AlurPendaftaran,
    BiayaPendidikan, Seragam, ContactPerson, SocialMedia, FAQ, Statistik, KMI,
    Program, Media, Dokumentasi, TenagaPengajar, BagianJabatan,
    InformasiTambahan, WhatsAppTemplate, WhatsAppTemplateKategori, Kontak
)
from admissions.models import Santri
from blog.models import Category, Tag, BlogPost, Testimoni, Pengumuman
from documents.models import DocumentTemplate
from payments.models import BankAccount, Payment

User = get_user_model()


class Command(BaseCommand):
    help = 'Membuat semua data dummy untuk semua aplikasi'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Jumlah data dummy untuk Santri, BlogPost, dll (default: 50)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus semua data sebelum membuat data baru'
        )

    def handle(self, *args, **options):
        count = options['count']
        clear = options.get('clear', False)
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('MEMBUAT SEMUA DATA DUMMY UNTUK SEMUA APLIKASI'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        if clear:
            self.stdout.write(self.style.WARNING('Menghapus data lama...'))
            self.clear_all_data()
        
        # 1. Buat akun demo
        self.stdout.write('\n[1/15] Membuat akun demo...')
        self.create_demo_accounts()
        
        # 2. Core App
        self.stdout.write('[2/15] Membuat data Core App...')
        self.create_core_data()
        
        # 3. Admissions (Santri)
        self.stdout.write(f'[3/15] Membuat {count} data Santri...')
        self.create_santri_data(count)
        
        # 4. Blog (Category, Tag, BlogPost)
        self.stdout.write(f'[4/15] Membuat data Blog ({count//2} posts)...')
        self.create_blog_data(count//2)
        
        # 5. Testimoni
        self.stdout.write(f'[5/15] Membuat {count//5} Testimoni...')
        self.create_testimoni_data(count//5)
        
        # 6. Pengumuman
        self.stdout.write(f'[6/15] Membuat {count//10} Pengumuman...')
        self.create_pengumuman_data(count//10)
        
        # 7. Documents (DocumentTemplate)
        self.stdout.write('[7/15] Membuat DocumentTemplate...')
        self.create_document_template_data()
        
        # 8. Payments (BankAccount, Payment)
        self.stdout.write('[8/15] Membuat data Payments...')
        self.create_payment_data()
        
        # 9. Tenaga Pengajar
        self.stdout.write('[9/15] Membuat Tenaga Pengajar...')
        self.create_tenaga_pengajar_data(25)
        
        # 10. Kontak (Inquiry)
        self.stdout.write(f'[10/15] Membuat {count//10} Kontak/Inquiry...')
        self.create_kontak_data(count//10)
        
        # Summary
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('SUMMARY DATA DUMMY'))
        self.stdout.write('=' * 70)
        self.show_summary()
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('SEMUA DATA DUMMY BERHASIL DIBUAT!'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('\nAkun Demo:'))
        self.stdout.write('  - Username: admin, Password: admin123 (Superadmin)')
        self.stdout.write('  - Username: petugas, Password: petugas123 (Petugas Pendaftaran)')
        self.stdout.write('  - Username: bendahara, Password: bendahara123 (Bendahara)')

    def clear_all_data(self):
        """Hapus semua data dummy"""
        Payment.objects.all().delete()
        BankAccount.objects.all().delete()
        Santri.objects.all().delete()
        BlogPost.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        Testimoni.objects.all().delete()
        Pengumuman.objects.all().delete()
        DocumentTemplate.objects.all().delete()
        Kontak.objects.all().delete()
        TenagaPengajar.objects.all().delete()
        BagianJabatan.objects.all().delete()
        # Core models
        Dokumentasi.objects.all().delete()
        Media.objects.all().delete()
        Program.objects.all().delete()
        Statistik.objects.all().delete()
        FAQ.objects.all().delete()
        SocialMedia.objects.all().delete()
        ContactPerson.objects.all().delete()
        Seragam.objects.all().delete()
        BiayaPendidikan.objects.all().delete()
        AlurPendaftaran.objects.all().delete()
        Persyaratan.objects.all().delete()
        JadwalHarian.objects.all().delete()
        Ekstrakurikuler.objects.all().delete()
        Fasilitas.objects.all().delete()
        KMI.objects.all().delete()
        ProgramPendidikan.objects.all().delete()
        SejarahTimeline.objects.all().delete()
        HeroSection.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('  Data lama berhasil dihapus.'))

    def create_demo_accounts(self):
        """Buat akun demo"""
        # Superadmin
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@pondok.id',
                'first_name': 'Administrator',
                'last_name': 'Pondok',
                'role': 'superadmin',
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'  [OK] Akun admin dibuat'))
        
        # Petugas Pendaftaran
        petugas, created = User.objects.get_or_create(
            username='petugas',
            defaults={
                'email': 'petugas@pondok.id',
                'first_name': 'Petugas',
                'last_name': 'Pendaftaran',
                'role': 'petugaspendaftaran',
                'is_staff': True,
                'is_active': True,
            }
        )
        if created:
            petugas.set_password('petugas123')
            petugas.save()
            self.stdout.write(self.style.SUCCESS(f'  [OK] Akun petugas dibuat'))
        
        # Bendahara
        bendahara, created = User.objects.get_or_create(
            username='bendahara',
            defaults={
                'email': 'bendahara@pondok.id',
                'first_name': 'Bendahara',
                'last_name': 'Pondok',
                'role': 'bendahara',
                'is_staff': True,
                'is_active': True,
            }
        )
        if created:
            bendahara.set_password('bendahara123')
            bendahara.save()
            self.stdout.write(self.style.SUCCESS(f'  [OK] Akun bendahara dibuat'))

    def create_core_data(self):
        """Buat data Core App (singleton dan basic data)"""
        # WebsiteSettings
        WebsiteSettings.objects.get_or_create(pk=1, defaults={
            'nama_pondok': 'PESANTREN MODERN RAUDHATUSSALAM',
            'alamat': 'Jalan Lintas Mahato-Cikampak Km. 24, Gambangan, Mahato',
            'no_telepon': '+62 852 6999 7007',
            'email': 'info@raudhatussalam.sch.id',
        })
        
        # VisiMisi
        VisiMisi.objects.get_or_create(pk=1, defaults={
            'visi': '<p>Sebagai lembaga pendidikan pencetak kader-kader pemimpin umat</p>',
            'misi': '<ul><li>Mempersiapkan pribadi umat yang berilmu pengetahuan</li></ul>',
        })
        
        # KMI
        KMI.objects.get_or_create(pk=1, defaults={
            'visi_kmi': '<p>Mewujudkan generasi beriman dan berilmu pengetahuan</p>',
            'profil_kmi': '<p>Kulliyatu-l-Mu\'allimin wal Mu\'alliat Al-Islamiyah</p>',
        })
        
        # Persyaratan
        Persyaratan.objects.get_or_create(pk=1, defaults={
            'persyaratan_santri': '<ol><li>Fotokopi kartu keluarga</li><li>Fotokopi akte kelahiran</li></ol>',
            'persyaratan_santriwati': '<ol><li>Fotokopi kartu keluarga</li><li>Fotokopi akte kelahiran</li></ol>',
        })
        
        # AlurPendaftaran
        AlurPendaftaran.objects.get_or_create(pk=1, defaults={
            'alur_pendaftaran': '<ol><li>Calon santri mendaftar</li><li>Membayar dana formulir</li></ol>',
        })
        
        self.stdout.write(self.style.SUCCESS('  [OK] Core data dibuat'))

    def create_santri_data(self, count):
        """Buat data Santri dummy"""
        nama_depan_laki = ['Ahmad', 'Muhammad', 'Ali', 'Hasan', 'Husain', 'Umar', 'Usman', 'Abdullah', 'Fadil', 'Rizki']
        nama_depan_perempuan = ['Fatimah', 'Aisyah', 'Khadijah', 'Zainab', 'Mariam', 'Nur', 'Siti', 'Putri', 'Sari', 'Dewi']
        nama_belakang = ['Rahman', 'Hakim', 'Nur', 'Sari', 'Hidayat', 'Maulana', 'Fauzi', 'Rizki', 'Pratama', 'Kurniawan']
        tempat_lahir = ['Jakarta', 'Bandung', 'Surabaya', 'Medan', 'Pekanbaru', 'Padang', 'Jambi', 'Palembang']
        asal_sekolah = ['SD Negeri 1', 'SD Islam Al-Azhar', 'MI Al-Ikhlas', 'SD Muhammadiyah', 'SDIT Nurul Iman']
        kelas_terakhir = ['Kelas 6', 'Kelas 5', 'Kelas 4']
        
        created = 0
        for i in range(count):
            jenis_kelamin = random.choice(['L', 'P'])
            if jenis_kelamin == 'L':
                nama_depan = random.choice(nama_depan_laki)
            else:
                nama_depan = random.choice(nama_depan_perempuan)
            
            nama_belakang_choice = random.choice(nama_belakang)
            nama_lengkap = f"{nama_depan} {nama_belakang_choice}"
            
            # Generate NISN unik
            nisn = f"{random.randint(1000000000, 9999999999)}"
            while Santri.objects.filter(nisn=nisn).exists():
                nisn = f"{random.randint(1000000000, 9999999999)}"
            
            # Generate tanggal lahir (usia 10-15 tahun)
            tahun_lahir = random.randint(2010, 2015)
            bulan_lahir = random.randint(1, 12)
            hari_lahir = random.randint(1, 28)
            tanggal_lahir = datetime(tahun_lahir, bulan_lahir, hari_lahir).date()
            
            # Generate status
            status = random.choice(['pending', 'verified', 'accepted', 'rejected'])
            
            santri = Santri.objects.create(
                nama_lengkap=nama_lengkap,
                nama_panggilan=nama_depan,
                nisn=nisn,
                tempat_lahir=random.choice(tempat_lahir),
                tanggal_lahir=tanggal_lahir,
                jenis_kelamin=jenis_kelamin,
                nama_ayah=f"Ayah {nama_lengkap}",
                nama_ibu=f"Ibu {nama_lengkap}",
                alamat=f"Jl. {random.choice(['Merdeka', 'Sudirman', 'Ahmad Yani'])} No. {random.randint(1, 999)}",
                no_hp=f"08{random.randint(100000000, 999999999)}",
                asal_sekolah=random.choice(asal_sekolah),
                kelas_terakhir=random.choice(kelas_terakhir),
                status=status,
            )
            created += 1
            if created % 10 == 0:
                self.stdout.write(f'  [OK] {created}/{count} santri dibuat...')
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] {created} santri dibuat'))

    def create_blog_data(self, count):
        """Buat data Blog (Category, Tag, BlogPost)"""
        # Categories
        categories_data = ['Pendidikan', 'Kegiatan', 'Pengumuman', 'Prestasi', 'Berita']
        categories = []
        for cat_name in categories_data:
            cat, _ = Category.objects.get_or_create(name=cat_name)
            categories.append(cat)
        
        # Tags
        tags_data = ['Pesantren', 'Santri', 'Pendidikan Islam', 'Kegiatan', 'Prestasi', 'Berita', 'Pengumuman']
        tags = []
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        
        # Blog Posts
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()
        
        titles = [
            'Kegiatan Khataman Al-Qur\'an Santri',
            'Prestasi Santri di Olimpiade Sains',
            'Acara Maulid Nabi di Pesantren',
            'Pembukaan Tahun Ajaran Baru',
            'Kegiatan Outbound Santri',
            'Lomba Tahfidz Al-Qur\'an',
            'Kunjungan Tamu Kehormatan',
            'Kegiatan Ekstrakurikuler Pramuka',
        ]
        
        created = 0
        for i in range(count):
            title = random.choice(titles) + f" {i+1}"
            content = f"<p>Ini adalah konten artikel tentang {title.lower()}. Artikel ini berisi informasi lengkap tentang kegiatan yang dilakukan di pesantren.</p>" * 5
            excerpt = f"Ringkasan artikel tentang {title.lower()}."
            
            post = BlogPost.objects.create(
                title=title,
                author=admin_user,
                content=content,
                excerpt=excerpt,
                category=random.choice(categories),
                status=random.choice(['draft', 'published', 'published', 'published']),  # 75% published
                published_at=timezone.now() - timedelta(days=random.randint(0, 90)),
                is_featured=random.choice([True, False, False, False]) if i < 5 else False,
            )
            post.tags.set(random.sample(tags, random.randint(2, 4)))
            created += 1
            if created % 5 == 0:
                self.stdout.write(f'  [OK] {created}/{count} blog posts dibuat...')
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] {created} blog posts, {len(categories)} categories, {len(tags)} tags dibuat'))

    def create_testimoni_data(self, count):
        """Buat data Testimoni"""
        nama_list = [
            'Ahmad Fauzi', 'Muhammad Rizki', 'Ali Rahman', 'Fatimah Sari',
            'Aisyah Nur', 'Khadijah Dewi', 'Hasan Maulana', 'Husain Pratama'
        ]
        jabatan_list = ['Alumni 2020', 'Alumni 2021', 'Alumni 2022', 'Wali Santri', 'Orang Tua Santri']
        testimoni_texts = [
            'Pesantren ini sangat baik untuk pendidikan anak saya. Anak saya menjadi lebih disiplin dan berakhlak mulia.',
            'Saya sangat puas dengan pendidikan di pesantren ini. Anak saya mendapatkan pendidikan agama dan umum yang seimbang.',
            'Pesantren Modern Raudhatussalam adalah pilihan terbaik untuk pendidikan anak. Fasilitas lengkap dan tenaga pengajar berkualitas.',
            'Anak saya sangat senang belajar di pesantren ini. Metode pembelajaran yang menarik dan menyenangkan.',
        ]
        
        created = 0
        for i in range(count):
            Testimoni.objects.create(
                nama=random.choice(nama_list) + f" {i+1}",
                jabatan=random.choice(jabatan_list),
                testimoni=random.choice(testimoni_texts),
                rating=random.randint(4, 5),
                is_published=True,
            )
            created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] {created} testimoni dibuat'))

    def create_pengumuman_data(self, count):
        """Buat data Pengumuman"""
        titles = [
            'Pengumuman Pendaftaran Santri Baru',
            'Jadwal Ujian Masuk Pesantren',
            'Pengumuman Hasil Seleksi',
            'Informasi Biaya Pendidikan',
            'Jadwal Kunjungan Orang Tua',
        ]
        
        created = 0
        for i in range(count):
            title = random.choice(titles) + f" {i+1}"
            content = f"<p>Ini adalah pengumuman tentang {title.lower()}.</p>" * 3
            
            Pengumuman.objects.create(
                judul=title,
                konten=content,
                status=random.choice(['draft', 'published', 'published']),
                is_penting=random.choice([True, False, False]),
                published_at=timezone.now() - timedelta(days=random.randint(0, 30)),
            )
            created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] {created} pengumuman dibuat'))

    def create_document_template_data(self):
        """Buat data DocumentTemplate"""
        templates_data = [
            {
                'nama': 'Formulir Pendaftaran',
                'slug': 'formulir-pendaftaran',
                'deskripsi': 'Template formulir pendaftaran santri baru',
                'html_template': '<h1>Formulir Pendaftaran</h1><p>Nama: {{nama_lengkap}}</p><p>NISN: {{nisn}}</p>',
            },
            {
                'nama': 'Surat Keterangan',
                'slug': 'surat-keterangan',
                'deskripsi': 'Template surat keterangan',
                'html_template': '<h1>Surat Keterangan</h1><p>Yang bertanda tangan di bawah ini menerangkan bahwa:</p><p>Nama: {{nama_lengkap}}</p>',
            },
        ]
        
        created = 0
        for data in templates_data:
            DocumentTemplate.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] {created} document templates dibuat'))

    def create_payment_data(self):
        """Buat data Payments (BankAccount, Payment)"""
        # Bank Accounts
        banks_data = [
            {'nama_bank': 'BCA', 'nomor_rekening': '1234567890', 'nama_pemilik_rekening': 'Pesantren Modern Raudhatussalam', 'biaya_pendaftaran': 250000},
            {'nama_bank': 'BRI', 'nomor_rekening': '0987654321', 'nama_pemilik_rekening': 'Pesantren Modern Raudhatussalam', 'biaya_pendaftaran': 250000},
            {'nama_bank': 'BSI', 'nomor_rekening': '1122334455', 'nama_pemilik_rekening': 'Pesantren Modern Raudhatussalam', 'biaya_pendaftaran': 250000},
        ]
        
        bank_accounts = []
        for data in banks_data:
            bank, _ = BankAccount.objects.get_or_create(
                nomor_rekening=data['nomor_rekening'],
                defaults=data
            )
            bank_accounts.append(bank)
        
        # Payments (hanya untuk santri yang sudah verified/accepted)
        santri_with_payment = Santri.objects.filter(status__in=['verified', 'accepted'])[:20]
        bendahara = User.objects.filter(role='bendahara').first()
        
        created = 0
        for santri in santri_with_payment:
            if not hasattr(santri, 'payment'):
                Payment.objects.create(
                    santri=santri,
                    bank_pengirim=random.choice(['BCA', 'BRI', 'BSI', 'Mandiri']),
                    nama_pemilik_rekening=santri.nama_ayah,
                    jumlah_transfer=250000,
                    status=random.choice(['pending', 'verified', 'verified']),
                    verified_by=bendahara if random.choice([True, False]) else None,
                )
                created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] {len(bank_accounts)} bank accounts, {created} payments dibuat'))

    def create_tenaga_pengajar_data(self, count):
        """Buat data Tenaga Pengajar"""
        # Bagian/Jabatan
        bagian_data = [
            {'nama': 'Pendiri', 'order': 1},
            {'nama': 'Pimpinan', 'order': 2},
            {'nama': 'Kepala Sekolah', 'order': 3},
            {'nama': 'Ustadz', 'order': 4},
            {'nama': 'Ustadzah', 'order': 5},
        ]
        
        bagian_objects = {}
        for data in bagian_data:
            bagian, _ = BagianJabatan.objects.get_or_create(
                nama=data['nama'],
                defaults={'order': data['order'], 'is_active': True}
            )
            bagian_objects[data['nama']] = bagian
        
        # Tenaga Pengajar
        nama_list = [
            'Ahmad Fauzi', 'Muhammad Rizki', 'Ali Rahman', 'Fatimah Sari',
            'Aisyah Nur', 'Khadijah Dewi', 'Hasan Maulana', 'Husain Pratama'
        ]
        
        created = 0
        for i in range(count):
            jenis_kelamin = random.choice(['L', 'P'])
            nama = random.choice(nama_list) + f" {i+1}"
            
            if jenis_kelamin == 'L':
                bagian = random.choice([bagian_objects['Pendiri'], bagian_objects['Pimpinan'], bagian_objects['Ustadz']])
            else:
                bagian = random.choice([bagian_objects['Pimpinan'], bagian_objects['Ustadzah']])
            
            TenagaPengajar.objects.create(
                nama_lengkap=nama,
                jenis_kelamin=jenis_kelamin,
                bagian_jabatan=bagian,
                tempat_lahir=random.choice(['Jakarta', 'Bandung', 'Medan']),
                pendidikan_terakhir=random.choice(['S1 Pendidikan Agama Islam', 'S1 Tafsir', 'S2 Pendidikan Islam']),
                bidang_keahlian=random.choice(['Tafsir', 'Hadits', 'Fiqih', 'Bahasa Arab']),
                is_published=True,
            )
            created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] {created} tenaga pengajar dibuat'))

    def create_kontak_data(self, count):
        """Buat data Kontak/Inquiry"""
        nama_list = ['Budi Santoso', 'Siti Nurhaliza', 'Ahmad Fauzi', 'Mariam Sari', 'Rizki Pratama']
        subjek_list = [
            'Pertanyaan tentang Pendaftaran',
            'Informasi Biaya Pendidikan',
            'Jadwal Kunjungan',
            'Fasilitas Pesantren',
            'Program Pendidikan',
        ]
        
        created = 0
        for i in range(count):
            Kontak.objects.create(
                nama=random.choice(nama_list) + f" {i+1}",
                email=f"kontak{i+1}@example.com",
                no_hp=f"08{random.randint(100000000, 999999999)}",
                subjek=random.choice(subjek_list),
                pesan=f"Ini adalah pesan inquiry tentang {random.choice(subjek_list).lower()}.",
                status=random.choice(['baru', 'dibaca', 'dibalas', 'selesai']),
            )
            created += 1
        
        self.stdout.write(self.style.SUCCESS(f'  [OK] {created} kontak/inquiry dibuat'))

    def show_summary(self):
        """Tampilkan summary data yang dibuat"""
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Santri: {Santri.objects.count()}')
        self.stdout.write(f'Blog Posts: {BlogPost.objects.count()}')
        self.stdout.write(f'Categories: {Category.objects.count()}')
        self.stdout.write(f'Tags: {Tag.objects.count()}')
        self.stdout.write(f'Testimoni: {Testimoni.objects.count()}')
        self.stdout.write(f'Pengumuman: {Pengumuman.objects.count()}')
        self.stdout.write(f'Document Templates: {DocumentTemplate.objects.count()}')
        self.stdout.write(f'Bank Accounts: {BankAccount.objects.count()}')
        self.stdout.write(f'Payments: {Payment.objects.count()}')
        self.stdout.write(f'Tenaga Pengajar: {TenagaPengajar.objects.count()}')
        self.stdout.write(f'Kontak/Inquiry: {Kontak.objects.count()}')
        self.stdout.write(f'WebsiteSettings: {WebsiteSettings.objects.count()}')
        self.stdout.write(f'FAQ: {FAQ.objects.count()}')
        self.stdout.write(f'Statistik: {Statistik.objects.count()}')

