"""
Management command untuk membuat semua data dummy sesuai index.html
Usage: python manage.py create_all_dummy_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
from django.utils.text import slugify
from core.models import (
    WebsiteSettings, HeroSection, SejarahTimeline, VisiMisi, ProgramPendidikan,
    Fasilitas, Ekstrakurikuler, JadwalHarian, Persyaratan, AlurPendaftaran,
    BiayaPendidikan, Seragam, ContactPerson, SocialMedia, FAQ, Statistik, KMI,
    ProgramPendidikanImage, SejarahTimelineImage, EkstrakurikulerImage,
    Program, Media, Dokumentasi, DokumentasiImage, TenagaPengajar, BagianJabatan,
    InformasiTambahan, WhatsAppTemplate, WhatsAppTemplateKategori, Kontak
)
from datetime import datetime, timedelta
from io import BytesIO
import random

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None

User = get_user_model()


class Command(BaseCommand):
    help = 'Membuat semua data dummy sesuai dengan index.html'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus semua data sebelum membuat data baru',
        )

    def handle(self, *args, **options):
        clear = options.get('clear', False)
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('MEMBUAT SEMUA DATA DUMMY'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        if clear:
            self.stdout.write(self.style.WARNING('Menghapus data lama...'))
            self.clear_all_data()
        
        # 1. Buat akun demo
        self.stdout.write('\n[1/20] Membuat akun demo...')
        self.create_demo_accounts()
        
        # 2. WebsiteSettings
        self.stdout.write('[2/20] Membuat WebsiteSettings...')
        self.create_website_settings()
        
        # 3. HeroSection
        self.stdout.write('[3/20] Membuat HeroSection...')
        self.create_hero_sections()
        
        # 4. SejarahTimeline
        self.stdout.write('[4/20] Membuat SejarahTimeline...')
        self.create_sejarah_timeline()
        
        # 5. VisiMisi
        self.stdout.write('[5/20] Membuat VisiMisi...')
        self.create_visi_misi()
        
        # 6. ProgramPendidikan
        self.stdout.write('[6/20] Membuat ProgramPendidikan...')
        self.create_program_pendidikan()
        
        # 7. KMI
        self.stdout.write('[7/20] Membuat KMI...')
        self.create_kmi()
        
        # 8. Fasilitas
        self.stdout.write('[8/20] Membuat Fasilitas...')
        self.create_fasilitas()
        
        # 9. Ekstrakurikuler
        self.stdout.write('[9/20] Membuat Ekstrakurikuler...')
        self.create_ekstrakurikuler()
        
        # 10. JadwalHarian
        self.stdout.write('[10/20] Membuat JadwalHarian...')
        self.create_jadwal_harian()
        
        # 11. Persyaratan
        self.stdout.write('[11/20] Membuat Persyaratan...')
        self.create_persyaratan()
        
        # 12. AlurPendaftaran
        self.stdout.write('[12/20] Membuat AlurPendaftaran...')
        self.create_alur_pendaftaran()
        
        # 13. BiayaPendidikan
        self.stdout.write('[13/20] Membuat BiayaPendidikan...')
        self.create_biaya_pendidikan()
        
        # 14. Seragam
        self.stdout.write('[14/20] Membuat Seragam...')
        self.create_seragam()
        
        # 15. ContactPerson
        self.stdout.write('[15/20] Membuat ContactPerson...')
        self.create_contact_person()
        
        # 16. SocialMedia
        self.stdout.write('[16/20] Membuat SocialMedia...')
        self.create_social_media()
        
        # 17. FAQ
        self.stdout.write('[17/20] Membuat FAQ...')
        self.create_faq()
        
        # 18. Statistik
        self.stdout.write('[18/20] Membuat Statistik...')
        self.create_statistik()
        
        # 19. Program
        self.stdout.write('[19/25] Membuat Program...')
        self.create_program()
        
        # 20. Media
        self.stdout.write('[20/25] Membuat Media...')
        self.create_media()
        
        # 21. Dokumentasi
        self.stdout.write('[21/25] Membuat Dokumentasi...')
        self.create_dokumentasi()
        
        # 22. BagianJabatan & TenagaPengajar
        self.stdout.write('[22/25] Membuat BagianJabatan & TenagaPengajar...')
        self.create_bagian_jabatan()
        self.create_tenaga_pengajar()
        
        # 23. InformasiTambahan
        self.stdout.write('[23/25] Membuat InformasiTambahan...')
        self.create_informasi_tambahan()
        
        # 24. WhatsAppTemplate
        self.stdout.write('[24/25] Membuat WhatsAppTemplate...')
        self.create_whatsapp_template()
        
        # 25. Jalankan management commands lainnya
        self.stdout.write('[25/25] Menjalankan management commands lainnya...')
        self.run_other_commands()
        
        # Summary
        self.stdout.write('Menampilkan summary...')
        self.show_summary()
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('SEMUA DATA DUMMY BERHASIL DIBUAT!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

    def generate_dummy_image(self, text, width=1200, height=675, bg_color=None):
        """
        Generate a simple placeholder image so Program/Dokumentasi tidak kosong.
        If Pillow is unavailable, return None so callers can skip image creation gracefully.
        """
        if Image is None:
            return None

        if bg_color is None:
            colors = [
                (46, 204, 113), (52, 152, 219), (155, 89, 182),
                (241, 196, 15), (230, 126, 34), (231, 76, 60),
                (26, 188, 156), (52, 73, 94)
            ]
            bg_color = random.choice(colors)

        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", size=48)
        except Exception:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=48)
            except Exception:
                font = ImageFont.load_default()

        # Wrap text roughly to fit width
        words = text.split()
        lines = []
        current = []
        max_width = width - 80
        for word in words:
            test_line = " ".join(current + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current.append(word)
            else:
                if current:
                    lines.append(" ".join(current))
                current = [word]
        if current:
            lines.append(" ".join(current))

        total_height = len(lines) * 60
        start_y = (height - total_height) // 2
        for idx, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            x = (width - (bbox[2] - bbox[0])) // 2
            y = start_y + idx * 60
            draw.text((x, y), line, fill=(255, 255, 255), font=font)

        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=90)
        file_name = f"{slugify(text) or 'image'}-{random.randint(1000, 9999)}.jpg"
        return ContentFile(img_io.getvalue(), name=file_name)

    def clear_all_data(self):
        """Hapus semua data dummy"""
        DokumentasiImage.objects.all().delete()
        Dokumentasi.objects.all().delete()
        Media.objects.all().delete()
        Program.objects.all().delete()
        TenagaPengajar.objects.all().delete()
        BagianJabatan.objects.all().delete()
        InformasiTambahan.objects.all().delete()
        WhatsAppTemplate.objects.all().delete()
        WhatsAppTemplateKategori.objects.all().delete()
        Kontak.objects.all().delete()
        Statistik.objects.all().delete()
        FAQ.objects.all().delete()
        SocialMedia.objects.all().delete()
        ContactPerson.objects.all().delete()
        Seragam.objects.all().delete()
        BiayaPendidikan.objects.all().delete()
        AlurPendaftaran.objects.all().delete()
        Persyaratan.objects.all().delete()
        JadwalHarian.objects.all().delete()
        EkstrakurikulerImage.objects.all().delete()
        Ekstrakurikuler.objects.all().delete()
        Fasilitas.objects.all().delete()
        KMI.objects.all().delete()
        ProgramPendidikanImage.objects.all().delete()
        ProgramPendidikan.objects.all().delete()
        SejarahTimelineImage.objects.all().delete()
        SejarahTimeline.objects.all().delete()
        HeroSection.objects.all().delete()
        VisiMisi.objects.all().delete()

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
            self.stdout.write(self.style.SUCCESS(f'  [OK] Akun admin dibuat (password: admin123)'))
        else:
            self.stdout.write(self.style.WARNING(f'  - Akun admin sudah ada'))
        
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
            self.stdout.write(self.style.SUCCESS(f'  [OK] Akun petugas dibuat (password: petugas123)'))
        else:
            self.stdout.write(self.style.WARNING(f'  - Akun petugas sudah ada'))
        
        # User Biasa
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@pondok.id',
                'first_name': 'Demo',
                'last_name': 'User',
                'role': 'user',
                'is_active': True,
            }
        )
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'  [OK] Akun demo dibuat (password: demo123)'))
        else:
            self.stdout.write(self.style.WARNING(f'  - Akun demo sudah ada'))

    def create_website_settings(self):
        """Buat WebsiteSettings sesuai index.html"""
        settings, created = WebsiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'nama_pondok': 'PESANTREN MODERN RAUDHATUSSALAM',
                'arabic_name': 'معهد روضة السلام للتربية الإسلامية الحديثة',
                'alamat': 'Jalan Lintas Mahato-Cikampak Km. 24, Gambangan, Mahato, Tambusai Utara, Rokan Hulu, Riau, 28558',
                'no_telepon': '+62 852 6999 7007',
                'email': 'info@raudhatussalam.sch.id',
                'hero_title': 'Pendaftaran Santri Baru',
                'hero_subtitle': '2025/2026',
                'hero_tagline': 'Membentuk Generasi Unggul yang Berkarakter Islami',
                'hero_cta_primary_text': 'DAFTAR SEKARANG!',
                'hero_cta_primary_link': 'https://forms.gle/bsW2G2iGXJ4eduiV8',
                'hero_cta_secondary_text': 'ALUR PENDAFTARAN',
                'hero_cta_secondary_link': '/PENGUMUMAN ALUR PENDAFTARAN.pdf',
                'lokasi_pendaftaran': 'Kantor Penerimaan Santri Baru (PSB)\nPesantren Modern Raudhatussalam, Gambangan, Mahato Km. 24, Tambusai Utara,\nRokan Hulu, Riau',
                'google_maps_link': 'https://maps.app.goo.gl/kaeDPb4p3irrRwSn8',
                'deskripsi': 'Pesantren Modern Raudhatussalam adalah lembaga pendidikan Islam terpadu yang mengintegrasikan pendidikan agama dan umum dengan sistem asrama.',
                'meta_title': 'Pendaftaran Santri Baru - Pesantren Modern Raudhatussalam',
                'meta_description': 'Pendaftaran santri baru tahun ajaran 2025/2026. Pesantren Modern Raudhatussalam membentuk generasi Qur\'ani yang berkarakter Islami.',
                'meta_keywords': 'pendaftaran santri, pesantren modern, raudhatussalam, mahato, rokan hulu, riau',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  [OK] WebsiteSettings dibuat'))
        else:
            self.stdout.write(self.style.WARNING(f'  - WebsiteSettings sudah ada'))

    def create_hero_sections(self):
        """Buat HeroSection sesuai index.html"""
        hero_data = [
            {
                'title': 'Gerbang Pesantren',
                'subtitle': 'Selamat Datang di Pesantren Modern Raudhatussalam',
                'image': 'img/gerbang.png',
                'order': 1,
                'is_active': True,
            },
            {
                'title': 'Asrama Pesantren',
                'subtitle': 'Fasilitas Asrama yang Nyaman untuk Santri',
                'image': 'img/rusunawa.png',
                'order': 2,
                'is_active': True,
            },
            {
                'title': 'Pimpinan Pesantren',
                'subtitle': 'Kepemimpinan yang Berpengalaman',
                'image': 'img/pimpinan.png',
                'order': 3,
                'is_active': True,
            },
        ]
        
        for data in hero_data:
            hero, created = HeroSection.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] HeroSection: {data["title"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] HeroSection: {data["title"]} sudah ada'))

    def create_sejarah_timeline(self):
        """Buat SejarahTimeline sesuai index.html"""
        timeline_data = [
            {
                'judul': 'Awal Mula',
                'icon': 'fas fa-history',
                'deskripsi': 'Bermula dari kunjungan Pimpinan Pondok Modern Darussalam Gontor Ponorogo Jawa Timur, Dr. K.H. Abdullah Syukry Zarkasyi, M.A. Meninjau langsung keberadaan lembaga-lembaga pendidikan yang ada di Mahato, maka beliau menyampaikan keinginannya akan mendirikan lembaga yang bernuansa islami kepada bapak H. Fajar Nasution.',
                'order': 1,
            },
            {
                'judul': 'Pertemuan Bersejarah',
                'icon': 'fas fa-handshake',
                'deskripsi': 'Cita-cita tersebut dimulai dengan pertemuan singkat yang dilaksanakan di masjid As-Salam Gambangan, di depan para jamaah masjid Dr. K.H. Abdullah Syukry Zarkasyi, M.A menyampaikan cita-citanya dan selanjutnya bapak H. Fajar Nasution merealisasikannya dengan mulai membangun gedung dan lingkungan pesantren secara perlahan.',
                'order': 2,
            },
            {
                'judul': 'Pendirian Resmi',
                'icon': 'fas fa-flag',
                'deskripsi': 'Pada tanggal 6 Jumadal Ula\' 1428 H bertepatan dengan 10 Juni 2008, bapak H. Fajar Nasution, ibu Hj. Sumiati, Drs. Hajarul Aswad Ritonga, Sukirno, Drs. Syahid Marqum, Drs. Maghfur Abdul Halim, M.Pd., Drs. Junaidi, H. Abdul Wahid Sulaiman, Lc., Drs. Basron Sudarsono, dan Suparwasesa, S.E, M.M menetapkan struktur kepengurusan, nama yayasan dan sekaligus dengan resmi memulai tahun ajaran 2008/2009.',
                'order': 3,
            },
        ]
        
        for data in timeline_data:
            timeline, created = SejarahTimeline.objects.get_or_create(
                judul=data['judul'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] SejarahTimeline: {data["judul"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - SejarahTimeline: {data["judul"]} sudah ada'))

    def create_visi_misi(self):
        """Buat VisiMisi sesuai index.html"""
        visi = '<p>Sebagai lembaga pendidikan pencetak kader-kader pemimpin umat, menjadi tempat ibadah talabul \'ilmi dan pengetahuan islam, bahasa Al-Qur\'an dan pengetahuan umum, dengan jiwa tetap berjiwa pondok.</p>'
        misi = '''<ul>
<li>Mempersiapkan pribadi umat yang berilmu pengetahuan, berakhlak mulia dan berkhidmat kepada agama, masyarakat, dan negara.</li>
<li>Mendidik dan mengembangkan generasi mu'min muslimin yang berbudi tinggi, berbadan sehat, berpengetahuan luas, dan berfikiran bebas, serta berkhidmat kepada masyarakat.</li>
<li>Mengajarkan ilmu pengetahuan agama dan umum secara seimbang menuju terbentuknya ulama yang intelek</li>
<li>Mewujudkan warga negara Indonesia yang berkepribadian Indonesia dan bertaqwa kepada Allah SWT</li>
</ul>'''
        
        visi_misi, created = VisiMisi.objects.get_or_create(
            pk=1,
            defaults={
                'visi': visi,
                'misi': misi,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  [OK] VisiMisi dibuat'))
        else:
            visi_misi.visi = visi
            visi_misi.misi = misi
            visi_misi.save()
            self.stdout.write(self.style.WARNING(f'  - VisiMisi sudah ada, diupdate'))

    def create_program_pendidikan(self):
        """Buat ProgramPendidikan sesuai index.html"""
        program_data = [
            {
                'nama': 'Sekolah Dasar Islam Terpadu (SDIT)',
                'akreditasi': 'B',
                'icon': 'fas fa-school',
                'order': 1,
            },
            {
                'nama': 'Madrasah Diniyah Takmiliyah Awaliyah (MDTA)',
                'akreditasi': '-',
                'icon': 'fas fa-book',
                'order': 2,
            },
            {
                'nama': 'Madrasah Tsanawiyah (MTs)',
                'akreditasi': 'B',
                'icon': 'fas fa-graduation-cap',
                'order': 3,
            },
            {
                'nama': 'Madrasah Aliyah (MA)',
                'akreditasi': 'B',
                'icon': 'fas fa-university',
                'order': 4,
            },
            {
                'nama': 'Perguruan tinggi (Universitas Darunnajah Jakarta)',
                'akreditasi': '-',
                'icon': 'fas fa-building',
                'order': 5,
            },
        ]
        
        for data in program_data:
            program, created = ProgramPendidikan.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] ProgramPendidikan: {data["nama"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - ProgramPendidikan: {data["nama"]} sudah ada'))

            # Tambah gambar utama jika belum ada
            if not program.gambar:
                image_file = self.generate_dummy_image(program.nama, width=1000, height=600)
                if image_file:
                    program.gambar.save(image_file.name, image_file, save=True)

            # Tambah galeri (maks 3) jika kosong
            if program.gambar_program.count() == 0:
                for idx in range(1, 4):
                    image_file = self.generate_dummy_image(f"{program.nama} {idx}", width=900, height=550)
                    if image_file:
                        ProgramPendidikanImage.objects.create(
                            program=program,
                            gambar=image_file,
                            alt_text=f"{program.nama} - Foto {idx}",
                            order=idx
                        )

    def create_kmi(self):
        """Buat KMI sesuai index.html"""
        visi_kmi = '<p>Mewujudkan generasi beriman dan berilmu pengetahuan serta mampu menghadapi tantangan global</p>'
        profil_kmi = '''<ul>
<li><strong>Kulliyatu-l-Mu'allimin wal Mu'alliat Al-Islamiyah (KMI)</strong> menawarkan program pendidikan 6 tahun untuk lulusan SD/MI, dan 3 tahun untuk lulusan SMP/MTs.</li>
<li><strong>Kurikulum terpadu.</strong> Mengintegrasikan kurikulum pesantren dengan kurikulum nasional, memberikan pendidikan seimbang dan berkualitas.</li>
<li><strong>Pengelolaan santri 24 jam.</strong> Dengan sistem pengelolaan santri selama 24 jam, KMI memastikan pendidikan yang menyeluruh, mencakup aspek intelektual, keterampilan, dan spiritualitas.</li>
<li><strong>Menyiapkan generasi berkualitas.</strong> Kami berkomitmen untuk menyiapkan generasi yang beraqidah shohihah, berakhlak mulia, gemar beribadah, berilmu, dan berjiwa terampil.</li>
<li><strong>Lulusan siap melanjutkan atau mengabdi.</strong> Lulusan KMI Raudhatussalam diharapkan mampu melanjutkan pendidikan ke perguruan tinggi ataupun aktif berperan di masyarakat dengan ilmu yang telah didapat.</li>
</ul>'''
        
        kmi, created = KMI.objects.get_or_create(
            pk=1,
            defaults={
                'visi_kmi': visi_kmi,
                'profil_kmi': profil_kmi,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  [OK] KMI dibuat'))
        else:
            # Update jika sudah ada
            kmi.visi_kmi = visi_kmi
            kmi.profil_kmi = profil_kmi
            kmi.save()
            self.stdout.write(self.style.WARNING(f'  - KMI sudah ada, diupdate'))

    def create_fasilitas(self):
        """Buat Fasilitas sesuai index.html"""
        fasilitas_data = [
            {'nama': 'Masjid', 'icon': 'fas fa-mosque', 'order': 1},
            {'nama': 'Ruang Kelas', 'icon': 'fas fa-chalkboard', 'order': 2},
            {'nama': 'Asrama', 'icon': 'fas fa-bed', 'order': 3},
            {'nama': 'Kamar Mandi', 'icon': 'fas fa-shower', 'order': 4},
            {'nama': 'Lab. Komputer', 'icon': 'fas fa-laptop', 'order': 5},
            {'nama': 'Lapangan Sepak Bola', 'icon': 'fas fa-futbol', 'order': 6},
            {'nama': 'Lapangan Basket', 'icon': 'fas fa-basketball-ball', 'order': 7},
            {'nama': 'Lapangan Voli', 'icon': 'fas fa-volleyball-ball', 'order': 8},
            {'nama': 'Lapangan Badminton', 'icon': 'fas fa-table-tennis', 'order': 9},
            {'nama': 'Lapangan Takraw', 'icon': 'fas fa-football-ball', 'order': 10},
            {'nama': 'Klinik Kesehatan', 'icon': 'fas fa-first-aid', 'order': 11},
            {'nama': 'Perpustakaan', 'icon': 'fas fa-book', 'order': 12},
        ]
        
        for data in fasilitas_data:
            fasilitas, created = Fasilitas.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Fasilitas: {data["nama"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Fasilitas: {data["nama"]} sudah ada'))

    def create_ekstrakurikuler(self):
        """Buat Ekstrakurikuler sesuai index.html"""
        ekstra_data = [
            {'nama': 'Kepramukaan', 'icon': 'fas fa-campground', 'order': 1},
            {'nama': 'Pidato 3 bahasa', 'icon': 'fas fa-microphone-alt', 'order': 2},
            {'nama': 'Kursus MC', 'icon': 'fas fa-user-tie', 'order': 3},
            {'nama': 'Jam\'iyyatu-l-qurra', 'icon': 'fas fa-book-reader', 'order': 4},
            {'nama': 'Jam\'iyyatu-l-khutoba', 'icon': 'fas fa-bullhorn', 'order': 5},
            {'nama': 'Klub sepak bola', 'icon': 'fas fa-futbol', 'order': 6},
            {'nama': 'Menari', 'icon': 'fas fa-walking', 'order': 7},
        ]
        
        for data in ekstra_data:
            ekstra, created = Ekstrakurikuler.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Ekstrakurikuler: {data["nama"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Ekstrakurikuler: {data["nama"]} sudah ada'))

    def create_jadwal_harian(self):
        """Buat JadwalHarian sesuai index.html"""
        jadwal_data = [
            {
                'waktu': '04.00-06.00',
                'judul': 'Aktivitas Pagi',
                'deskripsi': 'Sholat subuh berjamaah dilanjutkan dengan tadarus Al-Qur\'an, Muhadatsah dan juga piket kelas/olahraga',
                'kategori': 'santri',
                'order': 1,
            },
            {
                'waktu': '06.00-07.30',
                'judul': 'Persiapan Sekolah',
                'deskripsi': 'Mandi, sarapan pagi dan perisapan untuk berangkat ke sekolah',
                'kategori': 'santri',
                'order': 2,
            },
            {
                'waktu': '07.30-12.15',
                'judul': 'KBM Pagi',
                'deskripsi': 'Kegiatan belajar mengajar (KBM) di ruangan kelas',
                'kategori': 'santri',
                'order': 3,
            },
            {
                'waktu': '12.15-14.15',
                'judul': 'Istirahat Siang',
                'deskripsi': 'Sholat dzuhur berjamaah di kamar, dilanjutkan makan siang di dapur',
                'kategori': 'santri',
                'order': 4,
            },
            {
                'waktu': '14.15-15.00',
                'judul': 'KBM Siang',
                'deskripsi': 'Kegiatan belajar mengajar (KBM) di ruangan kelas',
                'kategori': 'santri',
                'order': 5,
            },
            {
                'waktu': '15.00-16.00',
                'judul': 'Aktivitas Ashar',
                'deskripsi': 'Sholat ashar berjamaah dilanjutkan dengan tadarus Al-Qur\'an',
                'kategori': 'santri',
                'order': 6,
            },
            {
                'waktu': '16.00-17.15',
                'judul': 'Ekstrakurikuler',
                'deskripsi': 'Olahraga atau kegiatan ekstrakurikuler sesuai dengan jadwal',
                'kategori': 'santri',
                'order': 7,
            },
            {
                'waktu': '17.15-17.45',
                'judul': 'Persiapan Magrib',
                'deskripsi': 'Mandi dan persiapan sholat magrib di masjid',
                'kategori': 'santri',
                'order': 8,
            },
            {
                'waktu': '17.45-19.00',
                'judul': 'Aktivitas Magrib',
                'deskripsi': 'Sholat magrib berjamaah di masjid, tadarus Al-Qur\'an dan dilanjutkan dengan makan malam di dapur',
                'kategori': 'santri',
                'order': 9,
            },
            {
                'waktu': '19.00-21.30',
                'judul': 'Belajar Malam',
                'deskripsi': 'Sholat isya berjamaah di kamar, dan dilanjutkan dengan belajar malam terbimbing',
                'kategori': 'santri',
                'order': 10,
            },
        ]
        
        for data in jadwal_data:
            jadwal, created = JadwalHarian.objects.get_or_create(
                waktu=data['waktu'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] JadwalHarian: {data["judul"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - JadwalHarian: {data["judul"]} sudah ada'))

    def create_persyaratan(self):
        """Buat Persyaratan sesuai index.html"""
        persyaratan_santri = '''<ol>
<li>Fotokopi kartu keluarga (KK) dan KTP kedua orangtua (dua lembar)</li>
<li>Fotokopi akte kelahiran (dua lembar)</li>
<li>Fotokopi ijazah/Surat keterangan lulus (SKL) dua lembar</li>
<li>Pasfoto 3x4 background merah (tiga lembar)</li>
<li>Berbadan sehat jasmani dan rohani</li>
<li>Sanggup bertempat tinggal di asrama yang telah disediakan</li>
</ol>
<h4>Mutasi:</h4>
<ol>
<li>Surat pindah dari sekolah asal atau Emis/Dapodik</li>
<li>Raport Negeri Legalisir 1 lembar</li>
</ol>'''
        persyaratan_santriwati = persyaratan_santri  # Sama untuk putri
        
        persyaratan, created = Persyaratan.objects.get_or_create(
            pk=1,
            defaults={
                'persyaratan_santri': persyaratan_santri,
                'persyaratan_santriwati': persyaratan_santriwati,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  [OK] Persyaratan dibuat'))
        else:
            persyaratan.persyaratan_santri = persyaratan_santri
            persyaratan.persyaratan_santriwati = persyaratan_santriwati
            persyaratan.save()
            self.stdout.write(self.style.WARNING(f'  - Persyaratan sudah ada, diupdate'))

    def create_alur_pendaftaran(self):
        """Buat AlurPendaftaran sesuai index.html"""
        alur_text = '''<ol>
<li>Calon santri mendaftar secara langsung/online</li>
<li>Membayar dana formulir/uang pangkal</li>
<li>Melengkapi formulir pendaftaran</li>
<li>Menyerahkan persyaratan dokumen ketika validasi di kantor PPSB</li>
</ol>
<p><em>*Pendaftaran online melalui admin whatsapp panitia penerimaan santri baru (PPSB)</em></p>'''
        
        alur, created = AlurPendaftaran.objects.get_or_create(
            pk=1,
            defaults={
                'alur_pendaftaran': alur_text,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  [OK] AlurPendaftaran dibuat'))
        else:
            alur.alur_pendaftaran = alur_text
            alur.save()
            self.stdout.write(self.style.WARNING(f'  - AlurPendaftaran sudah ada, diupdate'))

    def create_biaya_pendidikan(self):
        """Buat BiayaPendidikan sesuai index.html"""
        biaya_data = [
            # Biaya Tahunan
            {'tipe': 'tahunan', 'nama': 'Uang Pangkal', 'jumlah': 250000, 'keterangan': 'Biaya pendaftaran', 'order': 1},
            {'tipe': 'tahunan', 'nama': 'Uang Pembangunan', 'jumlah': 1500000, 'keterangan': 'Biaya pembangunan', 'order': 2},
            {'tipe': 'tahunan', 'nama': 'Uang Kertas', 'jumlah': 200000, 'keterangan': 'Biaya untuk 1 semester', 'order': 3},
            {'tipe': 'tahunan', 'nama': 'Uang Kegiatan', 'jumlah': 200000, 'keterangan': 'Biaya untuk 1 semester', 'order': 4},
            # Biaya Bulanan
            {'tipe': 'bulanan', 'nama': 'Uang SPP', 'jumlah': 200000, 'keterangan': 'Biaya bulanan', 'order': 1},
            {'tipe': 'bulanan', 'nama': 'Iuran Makan', 'jumlah': 600000, 'keterangan': 'Biaya bulanan', 'order': 2},
            {'tipe': 'bulanan', 'nama': 'Iuran Listrik & Air', 'jumlah': 50000, 'keterangan': 'Biaya bulanan', 'order': 3},
        ]
        
        for data in biaya_data:
            biaya, created = BiayaPendidikan.objects.get_or_create(
                nama=data['nama'],
                tipe=data['tipe'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] BiayaPendidikan: {data["nama"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - BiayaPendidikan: {data["nama"]} sudah ada'))

    def create_seragam(self):
        """Buat Seragam sesuai index.html"""
        seragam_data = [
            {'hari': 'Sab - Ahad', 'seragam_putra': 'Kemeja biru + celana hitam', 'seragam_putri': 'Hem putih + sakdress biru', 'order': 1},
            {'hari': 'Sen - Sel', 'seragam_putra': 'Kemeja putih + celana hitam', 'seragam_putri': 'Hem putih + sakdress hitam', 'order': 2},
            {'hari': 'Rab - Kam', 'seragam_putra': 'Kemeja hijau + celana hitam', 'seragam_putri': 'Hem putih + sakdress hijau', 'order': 3},
            {'hari': 'Jum\'at', 'seragam_putra': 'Pakaian sehari-hari (rapi & sopan)', 'seragam_putri': 'Pakaian sehari-hari (rapi & sopan)', 'order': 4},
        ]
        
        for data in seragam_data:
            seragam, created = Seragam.objects.get_or_create(
                hari=data['hari'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Seragam: {data["hari"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Seragam: {data["hari"]} sudah ada'))

    def create_contact_person(self):
        """Buat ContactPerson sesuai index.html"""
        contact_data = [
            {
                'nama': 'Ust. Mohd Hafiz, S.Th.I., M.Pd',
                'no_hp': '081226985992',
                'order': 1,
                'is_active': True,
            },
            {
                'nama': 'Ust. Irvan Noordianto, S.Pd.I',
                'no_hp': '081371913190',
                'order': 2,
                'is_active': True,
            },
        ]
        
        for data in contact_data:
            contact, created = ContactPerson.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] ContactPerson: {data["nama"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - ContactPerson: {data["nama"]} sudah ada'))

    def create_social_media(self):
        """Buat SocialMedia sesuai index.html"""
        social_data = [
            {
                'platform': 'instagram',
                'url': 'https://www.instagram.com/rds_mahato?igsh=MTI3N3l1M2swbnFsOA%3D%3D&utm_source=qr',
                'username': 'rds_mahato',
                'order': 1,
                'is_active': True,
            },
            {
                'platform': 'facebook',
                'url': 'https://www.facebook.com/RaudhatussalamMahato?mibextid=wwXIfr',
                'username': 'RaudhatussalamMahato',
                'order': 2,
                'is_active': True,
            },
            {
                'platform': 'tiktok',
                'url': 'https://www.tiktok.com/@rds_mahato?_t=ZS-8vYVJeCm3EN&_r=1',
                'username': '@rds_mahato',
                'order': 4,
                'is_active': True,
            },
        ]
        
        for data in social_data:
            social, created = SocialMedia.objects.get_or_create(
                platform=data['platform'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] SocialMedia: {data["platform"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - SocialMedia: {data["platform"]} sudah ada'))

    def create_faq(self):
        """Buat FAQ sesuai index.html"""
        faq_data = [
            {
                'pertanyaan': 'Apakah ada periode khusus untuk pendaftaran?',
                'jawaban': 'Pendaftaran santri baru untuk tahun ajaran 2025/2026 dibuka mulai Januari 2025 sampai Juli 2025. Namun, kuota terbatas, jadi disarankan untuk mendaftar lebih awal.',
                'kategori': 'Pendaftaran',
                'order': 1,
            },
            {
                'pertanyaan': 'Apakah ada ujian masuk untuk calon santri?',
                'jawaban': 'Ya, calon santri akan menjalani ujian seleksi yang meliputi tes kemampuan akademik, tes baca Al-Qur\'an, dan wawancara. Hasil tes akan diinformasikan paling lambat satu minggu setelah pelaksanaan.',
                'kategori': 'Pendaftaran',
                'order': 2,
            },
            {
                'pertanyaan': 'Apakah santri diperbolehkan membawa gadget/HP?',
                'jawaban': 'Untuk menjaga fokus belajar dan kedisiplinan, santri tidak diperbolehkan membawa gadget atau HP selama di pesantren. Komunikasi dengan orang tua dapat dilakukan melalui telepon pesantren atau pada saat kunjungan.',
                'kategori': 'Peraturan',
                'order': 3,
            },
            {
                'pertanyaan': 'Bagaimana jadwal kunjungan orang tua?',
                'jawaban': 'Jadwal kunjungan orang tua diadakan setiap bulan pada minggu pertama. Orang tua juga dapat berkunjung di luar jadwal tersebut dengan izin dari pihak pesantren.',
                'kategori': 'Kunjungan',
                'order': 4,
            },
            {
                'pertanyaan': 'Apakah tersedia beasiswa untuk santri berprestasi?',
                'jawaban': 'Ya, pesantren menyediakan beasiswa untuk santri berprestasi. Persyaratan dan ketentuan beasiswa dapat ditanyakan langsung kepada panitia pendaftaran.',
                'kategori': 'Beasiswa',
                'order': 5,
            },
            {
                'pertanyaan': 'Bagaimana dengan fasilitas kesehatan di pesantren?',
                'jawaban': 'Pesantren Modern Raudhatussalam memiliki klinik kesehatan dengan tenaga medis yang siap 24 jam. Untuk kasus yang memerlukan penanganan lebih lanjut, santri akan dirujuk ke rumah sakit terdekat dengan persetujuan wali santri.',
                'kategori': 'Fasilitas',
                'order': 6,
            },
        ]
        
        for data in faq_data:
            faq, created = FAQ.objects.get_or_create(
                pertanyaan=data['pertanyaan'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] FAQ: {data["pertanyaan"][:50]}...'))
            else:
                self.stdout.write(self.style.WARNING(f'  - FAQ: {data["pertanyaan"][:50]}... sudah ada'))

    def create_statistik(self):
        """Buat Statistik sesuai index.html"""
        statistik_data = [
            {'judul': 'Total Santri', 'nilai': '500', 'icon': 'fas fa-users', 'order': 1, 'is_published': True},
            {'judul': 'Tenaga Pengajar', 'nilai': '50', 'icon': 'fas fa-chalkboard-teacher', 'order': 2, 'is_published': True},
            {'judul': 'Program Pendidikan', 'nilai': '5', 'icon': 'fas fa-school', 'order': 3, 'is_published': True},
            {'judul': 'Fasilitas', 'nilai': '12', 'icon': 'fas fa-building', 'order': 4, 'is_published': True},
            {'judul': 'Ekstrakurikuler', 'nilai': '7', 'icon': 'fas fa-futbol', 'order': 5, 'is_published': True},
            {'judul': 'Tahun Berdiri', 'nilai': '2008', 'icon': 'fas fa-calendar', 'order': 6, 'is_published': True},
        ]
        
        for data in statistik_data:
            statistik, created = Statistik.objects.get_or_create(
                judul=data['judul'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Statistik: {data["judul"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Statistik: {data["judul"]} sudah ada'))

    def create_program(self):
        """Buat Program dummy"""
        program_data = [
            {
                'nama': 'Peringatan Hari Besar Islam',
                'deskripsi': 'Kegiatan peringatan hari besar Islam seperti Maulid Nabi, Isra Mi\'raj, dan lainnya.',
                'tanggal_mulai': timezone.now().date(),
                'tanggal_selesai': (timezone.now() + timedelta(days=7)).date(),
                'status': 'published',
                'is_featured': True,
                'order': 1,
                'meta_description': 'Peringatan hari besar Islam dengan berbagai rangkaian acara keagamaan.',
            },
            {
                'nama': 'Pekan Olahraga Santri',
                'deskripsi': 'Kompetisi olahraga antar kelas dan asrama untuk mengembangkan bakat dan sportivitas santri.',
                'tanggal_mulai': (timezone.now() + timedelta(days=30)).date(),
                'tanggal_selesai': (timezone.now() + timedelta(days=37)).date(),
                'status': 'published',
                'is_featured': True,
                'order': 2,
                'meta_description': 'Pekan olahraga santri untuk meningkatkan sportivitas dan kebugaran.',
            },
            {
                'nama': 'Khataman Al-Qur\'an',
                'deskripsi': 'Acara khataman Al-Qur\'an untuk santri yang telah menyelesaikan hafalan.',
                'tanggal_mulai': (timezone.now() + timedelta(days=60)).date(),
                'tanggal_selesai': (timezone.now() + timedelta(days=60)).date(),
                'status': 'published',
                'is_featured': False,
                'order': 3,
                'meta_description': 'Khataman Al-Qur\'an bersama para santri dan dewan asatidz.',
            },
        ]
        
        for data in program_data:
            program, created = Program.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Program: {data["nama"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Program: {data["nama"]} sudah ada'))

            # Tambah gambar placeholder jika belum ada
            if not program.gambar:
                image_file = self.generate_dummy_image(program.nama, width=1200, height=700)
                if image_file:
                    program.gambar.save(image_file.name, image_file, save=True)
    
    def create_media(self):
        """Buat Media dummy (Galeri & Video)"""
        media_data = [
            {
                'tipe': 'gallery',
                'judul': 'Galeri Kegiatan Pesantren',
                'sub_judul': 'Dokumentasi berbagai kegiatan di pesantren',
                'order': 1,
                'is_published': True,
            },
            {
                'tipe': 'gallery',
                'judul': 'Fasilitas Pesantren',
                'sub_judul': 'Fasilitas lengkap untuk mendukung pembelajaran',
                'order': 2,
                'is_published': True,
            },
            {
                'tipe': 'video',
                'judul': 'Video Profil Pesantren',
                'sub_judul': 'Kenali lebih dekat Pesantren Modern Raudhatussalam',
                'order': 3,
                'is_published': True,
            },
        ]
        
        for data in media_data:
            media, created = Media.objects.get_or_create(
                judul=data['judul'],
                tipe=data['tipe'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Media: {data["judul"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Media: {data["judul"]} sudah ada'))
    
    def create_dokumentasi(self):
        """Buat Dokumentasi dummy"""
        dokumentasi_data = [
            {
                'judul': 'Kegiatan Belajar Mengajar',
                'deskripsi': 'Dokumentasi kegiatan belajar mengajar di kelas dan asrama',
                'kategori': 'pembelajaran',
                'tanggal_kegiatan': timezone.now().date(),
                'lokasi': 'Pesantren Modern Raudhatussalam',
                'order': 1,
                'is_published': True,
            },
            {
                'judul': 'Acara Khataman Al-Qur\'an',
                'deskripsi': 'Dokumentasi acara khataman Al-Qur\'an santri',
                'kategori': 'acara',
                'tanggal_kegiatan': (timezone.now() - timedelta(days=30)).date(),
                'lokasi': 'Masjid Pesantren',
                'order': 2,
                'is_published': True,
            },
            {
                'judul': 'Ekstrakurikuler Pramuka',
                'deskripsi': 'Kegiatan ekstrakurikuler kepramukaan',
                'kategori': 'ekstrakurikuler',
                'tanggal_kegiatan': (timezone.now() - timedelta(days=15)).date(),
                'lokasi': 'Lapangan Pesantren',
                'order': 3,
                'is_published': True,
            },
        ]
        
        for data in dokumentasi_data:
            dokumentasi, created = Dokumentasi.objects.get_or_create(
                judul=data['judul'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Dokumentasi: {data["judul"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Dokumentasi: {data["judul"]} sudah ada'))

            # Lengkapi galeri dokumentasi jika kosong
            if dokumentasi.gambar_dokumentasi.count() == 0:
                for idx in range(1, 4):
                    image_file = self.generate_dummy_image(f"{data['judul']} {idx}", width=1280, height=720)
                    if image_file:
                        DokumentasiImage.objects.create(
                            dokumentasi=dokumentasi,
                            gambar=image_file,
                            alt_text=f"{data['judul']} - Foto {idx}",
                            order=idx
                        )
    
    def create_bagian_jabatan(self):
        """Buat BagianJabatan dummy"""
        bagian_data = [
            {'nama': 'Pendiri', 'deskripsi': 'Pendiri pesantren', 'order': 1},
            {'nama': 'Pimpinan', 'deskripsi': 'Pimpinan pesantren', 'order': 2},
            {'nama': 'Kepala Sekolah', 'deskripsi': 'Kepala sekolah', 'order': 3},
            {'nama': 'Ustadz', 'deskripsi': 'Tenaga pengajar putra', 'order': 4},
            {'nama': 'Ustadzah', 'deskripsi': 'Tenaga pengajar putri', 'order': 5},
        ]
        
        for data in bagian_data:
            bagian, created = BagianJabatan.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] BagianJabatan: {data["nama"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - BagianJabatan: {data["nama"]} sudah ada'))
    
    def create_tenaga_pengajar(self):
        """Buat TenagaPengajar dummy"""
        # Skip karena sudah ada command create_dummy_tenaga_pengajar
        self.stdout.write(self.style.WARNING('  - TenagaPengajar akan dibuat oleh command create_dummy_tenaga_pengajar'))
    
    def create_informasi_tambahan(self):
        """Buat InformasiTambahan dummy"""
        info_data = [
            {
                'judul': 'Waktu Pendaftaran',
                'deskripsi': 'Pendaftaran dibuka mulai Januari 2025 sampai Juli 2025. Kuota terbatas, segera daftar!',
                'icon': 'fas fa-calendar-check',
                'warna': 'green',
                'order': 1,
                'is_published': True,
            },
            {
                'judul': 'Dokumen yang Diperlukan',
                'deskripsi': 'Fotokopi KK, KTP orangtua, akte kelahiran, ijazah/SKL, dan pasfoto 3x4 background merah.',
                'icon': 'fas fa-file-alt',
                'warna': 'blue',
                'order': 2,
                'is_published': True,
            },
            {
                'judul': 'Biaya Pendaftaran',
                'deskripsi': 'Uang pangkal: Rp 250.000. Informasi lengkap biaya pendidikan dapat dilihat di halaman biaya.',
                'icon': 'fas fa-money-bill-wave',
                'warna': 'orange',
                'order': 3,
                'is_published': True,
            },
        ]
        
        for data in info_data:
            info, created = InformasiTambahan.objects.get_or_create(
                judul=data['judul'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] InformasiTambahan: {data["judul"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - InformasiTambahan: {data["judul"]} sudah ada'))
    
    def create_whatsapp_template(self):
        """Buat WhatsAppTemplate dummy"""
        # Buat kategori dulu
        kategori_data = [
            {'nama': 'Pendaftaran', 'deskripsi': 'Template untuk pendaftaran santri', 'order': 1},
            {'nama': 'Notifikasi', 'deskripsi': 'Template untuk notifikasi sistem', 'order': 2},
        ]
        
        for data in kategori_data:
            kategori, created = WhatsAppTemplateKategori.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] WhatsAppTemplateKategori: {data["nama"]}'))
        
        # Buat template
        template_data = [
            {
                'nama': 'Konfirmasi Pendaftaran',
                'kategori': WhatsAppTemplateKategori.objects.filter(nama='Pendaftaran').first(),
                'tipe': 'public',
                'pesan': 'Terima kasih {nama} telah mendaftar di Pesantren Modern Raudhatussalam. Nomor pendaftaran Anda: {nomor_pendaftaran}. Silakan lengkapi dokumen dan lakukan pembayaran.',
                'variabel': 'nama, nomor_pendaftaran',
                'order': 1,
            },
            {
                'nama': 'Notifikasi Pembayaran',
                'kategori': WhatsAppTemplateKategori.objects.filter(nama='Notifikasi').first(),
                'tipe': 'system',
                'pesan': 'Pembayaran Anda sebesar {jumlah} telah diterima. Terima kasih.',
                'variabel': 'jumlah',
                'order': 2,
            },
        ]
        
        for data in template_data:
            template, created = WhatsAppTemplate.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] WhatsAppTemplate: {data["nama"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - WhatsAppTemplate: {data["nama"]} sudah ada'))
    
    def run_other_commands(self):
        """Jalankan management commands lainnya"""
        from django.core.management import call_command
        
        commands = [
            ('create_dummy_tenaga_pengajar', {'count': 25}),
            ('create_dummy_banks', {}),
            ('generate_dummy_data', {'count': 10}),
            ('create_dummy_santri', {'count': 50}),
        ]
        
        for cmd, kwargs in commands:
            try:
                self.stdout.write(f'  Menjalankan: {cmd}...')
                call_command(cmd, **kwargs)
                self.stdout.write(self.style.SUCCESS(f'  [OK] {cmd} selesai'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [ERROR] {cmd} error: {e}'))

    def show_summary(self):
        """Tampilkan summary data yang dibuat"""
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('SUMMARY DATA DUMMY'))
        self.stdout.write('=' * 60)
        self.stdout.write(f'WebsiteSettings: {WebsiteSettings.objects.count()}')
        self.stdout.write(f'HeroSection: {HeroSection.objects.count()}')
        self.stdout.write(f'SejarahTimeline: {SejarahTimeline.objects.count()}')
        self.stdout.write(f'VisiMisi: {VisiMisi.objects.count()}')
        self.stdout.write(f'ProgramPendidikan: {ProgramPendidikan.objects.count()}')
        self.stdout.write(f'KMI: {KMI.objects.count()}')
        self.stdout.write(f'Fasilitas: {Fasilitas.objects.count()}')
        self.stdout.write(f'Ekstrakurikuler: {Ekstrakurikuler.objects.count()}')
        self.stdout.write(f'JadwalHarian: {JadwalHarian.objects.count()}')
        self.stdout.write(f'Persyaratan: {Persyaratan.objects.count()}')
        self.stdout.write(f'AlurPendaftaran: {AlurPendaftaran.objects.count()}')
        self.stdout.write(f'BiayaPendidikan: {BiayaPendidikan.objects.count()}')
        self.stdout.write(f'Seragam: {Seragam.objects.count()}')
        self.stdout.write(f'ContactPerson: {ContactPerson.objects.count()}')
        self.stdout.write(f'SocialMedia: {SocialMedia.objects.count()}')
        self.stdout.write(f'FAQ: {FAQ.objects.count()}')
        self.stdout.write(f'Statistik: {Statistik.objects.count()}')
        self.stdout.write(f'Program: {Program.objects.count()}')
        self.stdout.write(f'Media: {Media.objects.count()}')
        self.stdout.write(f'Dokumentasi: {Dokumentasi.objects.count()}')
        self.stdout.write(f'TenagaPengajar: {TenagaPengajar.objects.count()}')
        self.stdout.write(f'BagianJabatan: {BagianJabatan.objects.count()}')
        self.stdout.write(f'InformasiTambahan: {InformasiTambahan.objects.count()}')
        self.stdout.write(f'WhatsAppTemplate: {WhatsAppTemplate.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('\nAkun Demo:'))
        self.stdout.write('  - Username: admin, Password: admin123 (Superadmin)')
        self.stdout.write('  - Username: petugas, Password: petugas123 (Petugas Pendaftaran)')
        self.stdout.write('  - Username: demo, Password: demo123 (User Biasa)')

