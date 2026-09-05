"""
Management command untuk membuat data dummy lengkap semua pengaturan website
Pondok Pesantren Modern Raudhatussalam Mahato
Usage: python manage.py create_website_settings_dummy [--clear]
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random

from core.models import (
    WebsiteSettings, HeroSection, SejarahTimeline, VisiMisi, ProgramPendidikan,
    Fasilitas, Ekstrakurikuler, JadwalHarian, Persyaratan, AlurPendaftaran,
    BiayaPendidikan, Seragam, ContactPerson, SocialMedia, FAQ, Statistik, KMI,
    Program, Media, Dokumentasi, TenagaPengajar, BagianJabatan,
    InformasiTambahan, ProgramPendidikanImage, SejarahTimelineImage,
    EkstrakurikulerImage, DokumentasiImage
)


class Command(BaseCommand):
    help = 'Membuat data dummy lengkap semua pengaturan website Pondok Pesantren Modern Raudhatussalam Mahato'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus semua data sebelum membuat data baru'
        )

    def handle(self, *args, **options):
        clear = options.get('clear', False)
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('MEMBUAT DATA DUMMY PENGATURAN WEBSITE LENGKAP'))
        self.stdout.write(self.style.SUCCESS('Pondok Pesantren Modern Raudhatussalam Mahato'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        if clear:
            self.stdout.write(self.style.WARNING('Menghapus data lama...'))
            self.clear_all_data()
        
        # 1. WebsiteSettings
        self.stdout.write('\n[1/15] Membuat WebsiteSettings...')
        self.create_website_settings()
        
        # 2. HeroSection
        self.stdout.write('[2/15] Membuat HeroSection...')
        self.create_hero_sections()
        
        # 3. SejarahTimeline
        self.stdout.write('[3/15] Membuat SejarahTimeline...')
        self.create_sejarah_timeline()
        
        # 4. VisiMisi
        self.stdout.write('[4/15] Membuat VisiMisi...')
        self.create_visi_misi()
        
        # 5. ProgramPendidikan
        self.stdout.write('[5/15] Membuat ProgramPendidikan...')
        self.create_program_pendidikan()
        
        # 6. KMI
        self.stdout.write('[6/15] Membuat KMI...')
        self.create_kmi()
        
        # 7. Fasilitas
        self.stdout.write('[7/15] Membuat Fasilitas...')
        self.create_fasilitas()
        
        # 8. Ekstrakurikuler
        self.stdout.write('[8/15] Membuat Ekstrakurikuler...')
        self.create_ekstrakurikuler()
        
        # 9. JadwalHarian
        self.stdout.write('[9/15] Membuat JadwalHarian...')
        self.create_jadwal_harian()
        
        # 10. Persyaratan
        self.stdout.write('[10/15] Membuat Persyaratan...')
        self.create_persyaratan()
        
        # 11. AlurPendaftaran
        self.stdout.write('[11/15] Membuat AlurPendaftaran...')
        self.create_alur_pendaftaran()
        
        # 12. BiayaPendidikan
        self.stdout.write('[12/15] Membuat BiayaPendidikan...')
        self.create_biaya_pendidikan()
        
        # 13. Seragam
        self.stdout.write('[13/15] Membuat Seragam...')
        self.create_seragam()
        
        # 14. ContactPerson
        self.stdout.write('[14/15] Membuat ContactPerson...')
        self.create_contact_person()
        
        # 15. SocialMedia, FAQ, Statistik, InformasiTambahan
        self.stdout.write('[15/15] Membuat SocialMedia, FAQ, Statistik, InformasiTambahan...')
        self.create_social_media()
        self.create_faq()
        self.create_statistik()
        self.create_informasi_tambahan()
        
        # Summary
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('SUMMARY DATA DUMMY PENGATURAN WEBSITE'))
        self.stdout.write('=' * 70)
        self.show_summary()
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('DATA DUMMY PENGATURAN WEBSITE BERHASIL DIBUAT!'))
        self.stdout.write(self.style.SUCCESS('=' * 70))

    def clear_all_data(self):
        """Hapus semua data pengaturan website"""
        DokumentasiImage.objects.all().delete()
        Dokumentasi.objects.all().delete()
        Media.objects.all().delete()
        Program.objects.all().delete()
        InformasiTambahan.objects.all().delete()
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
        WebsiteSettings.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('  Data lama berhasil dihapus.'))

    def create_website_settings(self):
        """Buat WebsiteSettings lengkap"""
        settings, created = WebsiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'nama_pondok': 'PESANTREN MODERN RAUDHATUSSALAM',
                'arabic_name': 'معهد روضة السلام للتربية الإسلامية الحديثة',
                'alamat': 'Jalan Lintas Mahato-Cikampak Km. 24, Gambangan, Mahato, Tambusai Utara, Rokan Hulu, Riau, 28558',
                'no_telepon': '+62 852 6999 7007',
                'email': 'info@raudhatussalam.sch.id',
                'website': 'https://rdsmahato.ponpes.id',
                'facebook': 'https://www.facebook.com/RaudhatussalamMahato',
                'instagram': 'https://www.instagram.com/rds_mahato',
                'tiktok': 'https://www.tiktok.com/@rds_mahato',
                'hero_title': 'Pendaftaran Santri Baru',
                'hero_subtitle': '2025/2026',
                'hero_tagline': 'Membentuk Generasi Unggul yang Berkarakter Islami',
                'hero_cta_primary_text': 'DAFTAR SEKARANG!',
                'hero_cta_primary_link': 'https://forms.gle/bsW2G2iGXJ4eduiV8',
                'hero_cta_secondary_text': 'ALUR PENDAFTARAN',
                'hero_cta_secondary_link': '/PENGUMUMAN ALUR PENDAFTARAN.pdf',
                'lokasi_pendaftaran': '''Kantor Penerimaan Santri Baru (PSB)
Pesantren Modern Raudhatussalam
Gambangan, Mahato Km. 24
Tambusai Utara, Rokan Hulu, Riau''',
                'google_maps_link': 'https://maps.app.goo.gl/kaeDPb4p3irrRwSn8',
                'google_maps_embed_code': '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3989.1234567890!2d100.123456!3d0.123456!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMMKwMDcnMjQuNCJOIDEwMMKwMDcnMjQuNCJF!5e0!3m2!1sid!2sid!4v1234567890123!5m2!1sid!2sid" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
                'deskripsi': '''Pesantren Modern Raudhatussalam adalah lembaga pendidikan Islam terpadu yang mengintegrasikan pendidikan agama dan umum dengan sistem asrama. Didirikan pada tahun 2008, pesantren ini merupakan salah satu pesantren alumni Gontor di wilayah Riau yang berkomitmen membentuk generasi Qur'ani yang berkarakter Islami.

Pesantren Modern Raudhatussalam menawarkan program pendidikan lengkap mulai dari SDIT, MDTA, MTs, MA, hingga perguruan tinggi. Dengan kurikulum terpadu yang mengintegrasikan kurikulum pesantren dan kurikulum nasional, pesantren ini menyiapkan santri untuk menjadi ulama yang intelek dan intelek yang ulama.''',
                'meta_title': 'Pendaftaran Santri Baru - Pesantren Modern Raudhatussalam Mahato',
                'meta_description': 'Pendaftaran santri baru tahun ajaran 2025/2026. Pesantren Modern Raudhatussalam Mahato membentuk generasi Qur\'ani yang berkarakter Islami. Lokasi: Mahato, Tambusai Utara, Rokan Hulu, Riau.',
                'meta_keywords': 'pendaftaran santri, pesantren modern, raudhatussalam, mahato, rokan hulu, riau, pesantren gontor, pendidikan islam terpadu, SDIT, MDTA, MTs, MA',
                'maintenance_mode': False,
                'maintenance_message': 'Website sedang dalam perawatan. Kami akan kembali segera.',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('  [OK] WebsiteSettings dibuat'))
        else:
            # Update dengan data lengkap
            for key, value in {
                'nama_pondok': 'PESANTREN MODERN RAUDHATUSSALAM',
                'arabic_name': 'معهد روضة السلام للتربية الإسلامية الحديثة',
                'alamat': 'Jalan Lintas Mahato-Cikampak Km. 24, Gambangan, Mahato, Tambusai Utara, Rokan Hulu, Riau, 28558',
                'no_telepon': '+62 852 6999 7007',
                'email': 'info@raudhatussalam.sch.id',
                'website': 'https://rdsmahato.ponpes.id',
                'facebook': 'https://www.facebook.com/RaudhatussalamMahato',
                'instagram': 'https://www.instagram.com/rds_mahato',
                'tiktok': 'https://www.tiktok.com/@rds_mahato',
            }.items():
                setattr(settings, key, value)
            settings.save()
            self.stdout.write(self.style.WARNING('  [-] WebsiteSettings sudah ada, diupdate'))

    def create_hero_sections(self):
        """Buat HeroSection"""
        hero_data = [
            {
                'title': 'Gerbang Pesantren',
                'subtitle': 'Selamat Datang di Pesantren Modern Raudhatussalam',
                'order': 1,
                'is_active': True,
            },
            {
                'title': 'Asrama Pesantren',
                'subtitle': 'Fasilitas Asrama yang Nyaman untuk Santri',
                'order': 2,
                'is_active': True,
            },
            {
                'title': 'Pimpinan Pesantren',
                'subtitle': 'Kepemimpinan yang Berpengalaman',
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

    def create_sejarah_timeline(self):
        """Buat SejarahTimeline"""
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

    def create_visi_misi(self):
        """Buat VisiMisi"""
        visi = '<p>Sebagai lembaga pendidikan pencetak kader-kader pemimpin umat, menjadi tempat ibadah talabul \'ilmi dan pengetahuan islam, bahasa Al-Qur\'an dan pengetahuan umum, dengan jiwa tetap berjiwa pondok.</p>'
        misi = '''<ul>
<li>Mempersiapkan pribadi umat yang berilmu pengetahuan, berakhlak mulia dan berkhidmat kepada agama, masyarakat, dan negara.</li>
<li>Mendidik dan mengembangkan generasi mu'min muslimin yang berbudi tinggi, berbadan sehat, berpengetahuan luas, dan berfikiran bebas, serta berkhidmat kepada masyarakat.</li>
<li>Mengajarkan ilmu pengetahuan agama dan umum secara seimbang menuju terbentuknya ulama yang intelek</li>
<li>Mewujudkan warga negara Indonesia yang berkepribadian Indonesia dan bertaqwa kepada Allah SWT</li>
</ul>'''
        
        visi_misi, created = VisiMisi.objects.get_or_create(
            pk=1,
            defaults={'visi': visi, 'misi': misi}
        )
        if not created:
            visi_misi.visi = visi
            visi_misi.misi = misi
            visi_misi.save()
        self.stdout.write(self.style.SUCCESS('  [OK] VisiMisi dibuat'))

    def create_program_pendidikan(self):
        """Buat ProgramPendidikan"""
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
                'nama': 'Perguruan Tinggi (Universitas Darunnajah Jakarta)',
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

    def create_kmi(self):
        """Buat KMI"""
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
            defaults={'visi_kmi': visi_kmi, 'profil_kmi': profil_kmi}
        )
        if not created:
            kmi.visi_kmi = visi_kmi
            kmi.profil_kmi = profil_kmi
            kmi.save()
        self.stdout.write(self.style.SUCCESS('  [OK] KMI dibuat'))

    def create_fasilitas(self):
        """Buat Fasilitas"""
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

    def create_ekstrakurikuler(self):
        """Buat Ekstrakurikuler"""
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

    def create_jadwal_harian(self):
        """Buat JadwalHarian"""
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

    def create_persyaratan(self):
        """Buat Persyaratan"""
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
        persyaratan_santriwati = persyaratan_santri
        
        persyaratan, created = Persyaratan.objects.get_or_create(
            pk=1,
            defaults={
                'persyaratan_santri': persyaratan_santri,
                'persyaratan_santriwati': persyaratan_santriwati,
            }
        )
        if not created:
            persyaratan.persyaratan_santri = persyaratan_santri
            persyaratan.persyaratan_santriwati = persyaratan_santriwati
            persyaratan.save()
        self.stdout.write(self.style.SUCCESS('  [OK] Persyaratan dibuat'))

    def create_alur_pendaftaran(self):
        """Buat AlurPendaftaran"""
        alur_text = '''<ol>
<li>Calon santri mendaftar secara langsung/online</li>
<li>Membayar dana formulir/uang pangkal</li>
<li>Melengkapi formulir pendaftaran</li>
<li>Menyerahkan persyaratan dokumen ketika validasi di kantor PPSB</li>
</ol>
<p><em>*Pendaftaran online melalui admin whatsapp panitia penerimaan santri baru (PPSB)</em></p>'''
        
        alur, created = AlurPendaftaran.objects.get_or_create(
            pk=1,
            defaults={'alur_pendaftaran': alur_text}
        )
        if not created:
            alur.alur_pendaftaran = alur_text
            alur.save()
        self.stdout.write(self.style.SUCCESS('  [OK] AlurPendaftaran dibuat'))

    def create_biaya_pendidikan(self):
        """Buat BiayaPendidikan"""
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

    def create_seragam(self):
        """Buat Seragam"""
        seragam_data = [
            {'hari': 'Sab - Ahad', 'kategori': 'santri', 'seragam_putra': 'Kemeja biru + celana hitam', 'seragam_putri': 'Hem putih + sakdress biru', 'order': 1},
            {'hari': 'Sen - Sel', 'kategori': 'santri', 'seragam_putra': 'Kemeja putih + celana hitam', 'seragam_putri': 'Hem putih + sakdress hitam', 'order': 2},
            {'hari': 'Rab - Kam', 'kategori': 'santri', 'seragam_putra': 'Kemeja hijau + celana hitam', 'seragam_putri': 'Hem putih + sakdress hijau', 'order': 3},
            {'hari': 'Jum\'at', 'kategori': 'santri', 'seragam_putra': 'Pakaian sehari-hari (rapi & sopan)', 'seragam_putri': 'Pakaian sehari-hari (rapi & sopan)', 'order': 4},
        ]
        
        for data in seragam_data:
            seragam, created = Seragam.objects.get_or_create(
                hari=data['hari'],
                kategori=data['kategori'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Seragam: {data["hari"]}'))

    def create_contact_person(self):
        """Buat ContactPerson"""
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

    def create_social_media(self):
        """Buat SocialMedia"""
        social_data = [
            {
                'platform': 'instagram',
                'url': 'https://www.instagram.com/rds_mahato',
                'username': 'rds_mahato',
                'order': 1,
                'is_active': True,
            },
            {
                'platform': 'facebook',
                'url': 'https://www.facebook.com/RaudhatussalamMahato',
                'username': 'RaudhatussalamMahato',
                'order': 2,
                'is_active': True,
            },
            {
                'platform': 'tiktok',
                'url': 'https://www.tiktok.com/@rds_mahato',
                'username': '@rds_mahato',
                'order': 3,
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

    def create_faq(self):
        """Buat FAQ"""
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

    def create_statistik(self):
        """Buat Statistik"""
        statistik_data = [
            {'judul': 'Total Santri', 'nilai': '500', 'icon': 'fas fa-users', 'warna': 'green', 'order': 1, 'is_published': True},
            {'judul': 'Tenaga Pengajar', 'nilai': '50', 'icon': 'fas fa-chalkboard-teacher', 'warna': 'blue', 'order': 2, 'is_published': True},
            {'judul': 'Program Pendidikan', 'nilai': '5', 'icon': 'fas fa-school', 'warna': 'purple', 'order': 3, 'is_published': True},
            {'judul': 'Fasilitas', 'nilai': '12', 'icon': 'fas fa-building', 'warna': 'orange', 'order': 4, 'is_published': True},
            {'judul': 'Ekstrakurikuler', 'nilai': '7', 'icon': 'fas fa-futbol', 'warna': 'red', 'order': 5, 'is_published': True},
            {'judul': 'Tahun Berdiri', 'nilai': '2008', 'icon': 'fas fa-calendar', 'warna': 'green', 'order': 6, 'is_published': True},
        ]
        
        for data in statistik_data:
            statistik, created = Statistik.objects.get_or_create(
                judul=data['judul'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Statistik: {data["judul"]}'))

    def create_informasi_tambahan(self):
        """Buat InformasiTambahan"""
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

    def show_summary(self):
        """Tampilkan summary"""
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
        self.stdout.write(f'InformasiTambahan: {InformasiTambahan.objects.count()}')

