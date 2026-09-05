"""
Management command untuk generate data dummy untuk Blog, Testimoni, dan Pengumuman
Usage: python manage.py generate_dummy_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.conf import settings
from blog.models import Category, Tag, BlogPost, BlogImage, Testimoni, Pengumuman
from datetime import timedelta
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate data dummy untuk Blog, Testimoni, dan Pengumuman (minimal 15 untuk masing-masing)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=25,
            help='Jumlah data yang akan dibuat untuk masing-masing model (default: 25)',
        )
        parser.add_argument(
            '--blog-only',
            action='store_true',
            help='Hanya membuat artikel blog saja',
        )

    def handle(self, *args, **options):
        count = options['count']
        blog_only = options.get('blog_only', False)
        
        self.stdout.write(self.style.SUCCESS(f'Memulai generate data dummy...'))
        
        # Get atau create admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('Tidak ada user admin ditemukan. Silakan buat user admin terlebih dahulu.'))
            return
        
        # Generate Categories
        self.stdout.write('Membuat Kategori...')
        categories = self.create_categories()
        
        # Generate Tags
        self.stdout.write('Membuat Tags...')
        tags = self.create_tags()
        
        # Generate Blog Posts
        self.stdout.write(f'Membuat {count} Artikel Blog dengan gambar...')
        self.create_blog_posts(count, admin_user, categories, tags)
        
        if not blog_only:
            # Generate Testimoni
            self.stdout.write(f'Membuat {count} Testimoni...')
            self.create_testimoni(count)
            
            # Generate Pengumuman
            self.stdout.write(f'Membuat {count} Pengumuman...')
            self.create_pengumuman(count)
        
        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] Data dummy berhasil dibuat!'))
        self.stdout.write(f'   - Kategori: {len(categories)}')
        self.stdout.write(f'   - Tags: {len(tags)}')
        self.stdout.write(f'   - Artikel Blog: {count}')
        if not blog_only:
            self.stdout.write(f'   - Testimoni: {count}')
            self.stdout.write(f'   - Pengumuman: {count}')

    def _strip_html(self, text):
        """Helper method untuk menghapus HTML tags dari text"""
        return strip_tags(text).strip()
    
    def generate_dummy_image(self, text, width=1200, height=600, bg_color=None, text_color=(50, 50, 50)):
        """Generate dummy image dengan text"""
        if bg_color is None:
            # Random color yang menarik
            colors = [
                (240, 248, 255),  # Alice Blue
                (255, 250, 240),  # Floral White
                (240, 255, 240),  # Honeydew
                (255, 245, 238),  # Seashell
                (240, 255, 255),  # Azure
                (255, 250, 250),  # Snow
                (248, 248, 255),  # Ghost White
                (245, 255, 250),  # Mint Cream
            ]
            bg_color = random.choice(colors)
        
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default if not available
        try:
            font_size = 60
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 60)
            except:
                font = ImageFont.load_default()
        
        # Split text into lines if too long
        words = text.split()
        lines = []
        current_line = []
        max_width = width - 100
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate total height
        line_height = 80
        total_height = len(lines) * line_height
        start_y = (height - total_height) // 2
        
        # Draw each line
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + (i * line_height)
            draw.text((x, y), line, fill=text_color, font=font)
        
        # Save to BytesIO
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=90)
        img_io.seek(0)
        return ContentFile(img_io.read())
    
    def create_categories(self):
        """Membuat kategori untuk blog"""
        category_names = [
            'Pendidikan', 'Kegiatan', 'Prestasi', 'Berita', 'Pengumuman',
            'Kegiatan Harian', 'Ekstrakurikuler', 'Kajian', 'Kegiatan Rutin',
            'Informasi Umum'
        ]
        
        categories = []
        for name in category_names:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'  [OK] Kategori "{name}" dibuat')
        
        return categories

    def create_tags(self):
        """Membuat tags untuk blog"""
        tag_names = [
            'Pondok Pesantren', 'Santri', 'Pendidikan Islam', 'Kegiatan', 'Prestasi',
            'Alumni', 'Kajian', 'Ekstrakurikuler', 'Berita', 'Pengumuman',
            'Kegiatan Harian', 'Kegiatan Rutin', 'Informasi', 'Acara', 'Event'
        ]
        
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            tags.append(tag)
            if created:
                self.stdout.write(f'  [OK] Tag "{name}" dibuat')
        
        return tags

    def create_blog_posts(self, count, author, categories, tags):
        """Membuat artikel blog"""
        titles = [
            'Kegiatan Rutin Sholat Berjamaah di Pondok Pesantren',
            'Prestasi Santri dalam Lomba Pidato Bahasa Arab',
            'Kajian Kitab Kuning Setiap Malam Jumat',
            'Kegiatan Ekstrakurikuler Pramuka untuk Santri',
            'Penerimaan Santri Baru Tahun Ajaran 2024',
            'Kegiatan Outbound Santri di Gunung Lawu',
            'Prestasi Santri dalam Olimpiade Matematika',
            'Kegiatan Tahfidz Al-Quran untuk Santri',
            'Kegiatan Bakti Sosial Santri ke Panti Asuhan',
            'Peringatan Maulid Nabi Muhammad SAW',
            'Kegiatan Muhadhoroh (Latihan Pidato) Santri',
            'Prestasi Santri dalam Lomba MTQ',
            'Kegiatan Rutin Tadarus Al-Quran',
            'Kegiatan Ekstrakurikuler Kaligrafi',
            'Kunjungan Santri ke Museum Sejarah',
            'Kegiatan Rutin Sholat Dhuha Berjamaah',
            'Prestasi Santri dalam Lomba Cerdas Cermat',
            'Kegiatan Ekstrakurikuler Pencak Silat',
            'Kegiatan Rutin Sholat Tahajud',
            'Peringatan Isra Mi\'raj Nabi Muhammad SAW',
            'Kegiatan Rutin Sholat Subuh Berjamaah',
            'Prestasi Santri dalam Lomba Debat Bahasa Inggris',
            'Kegiatan Ekstrakurikuler Seni Musik Islami',
            'Kegiatan Rutin Kajian Tafsir Al-Quran',
            'Prestasi Santri dalam Lomba Robotik',
            'Kegiatan Ekstrakurikuler Futsal untuk Santri',
            'Kegiatan Rutin Sholat Maghrib Berjamaah',
            'Prestasi Santri dalam Lomba Karya Tulis Ilmiah',
            'Kegiatan Ekstrakurikuler Bahasa Asing',
            'Kegiatan Rutin Kajian Hadits',
        ]
        
        contents = [
            '''<p>Pondok Pesantren kami mengadakan kegiatan rutin sholat berjamaah setiap hari. Kegiatan ini bertujuan untuk membiasakan santri dalam melaksanakan sholat tepat waktu dan berjamaah.</p>
            <p>Kegiatan sholat berjamaah ini diikuti oleh seluruh santri dan ustadz/ustadzah. Setiap santri diwajibkan untuk mengikuti kegiatan ini sebagai bagian dari pendidikan karakter dan akhlak.</p>
            <p>Dengan kegiatan ini, diharapkan santri dapat terbiasa dengan sholat berjamaah dan memahami pentingnya sholat dalam kehidupan sehari-hari.</p>''',
            
            '''<p>Alhamdulillah, beberapa santri kami berhasil meraih prestasi dalam lomba pidato bahasa Arab tingkat regional. Prestasi ini merupakan hasil dari kerja keras dan dedikasi santri dalam belajar bahasa Arab.</p>
            <p>Lomba ini diikuti oleh berbagai pondok pesantren di wilayah Jawa Tengah. Santri kami berhasil meraih juara 1, 2, dan 3 dalam berbagai kategori.</p>
            <p>Prestasi ini menjadi motivasi bagi santri lainnya untuk terus belajar dan berprestasi dalam berbagai bidang.</p>''',
            
            '''<p>Setiap malam Jumat, pondok pesantren mengadakan kajian kitab kuning yang diikuti oleh seluruh santri. Kajian ini membahas berbagai kitab klasik yang menjadi rujukan dalam pendidikan Islam.</p>
            <p>Kajian dipimpin oleh ustadz senior yang memiliki keahlian dalam bidang ilmu agama. Santri diajarkan untuk membaca, memahami, dan mengamalkan isi kitab yang dikaji.</p>
            <p>Kegiatan ini merupakan bagian dari kurikulum pendidikan pondok pesantren yang bertujuan untuk memperdalam pemahaman santri tentang ajaran Islam.</p>''',
            
            '''<p>Ekstrakurikuler pramuka menjadi salah satu kegiatan favorit santri. Kegiatan ini mengajarkan nilai-nilai kepemimpinan, kedisiplinan, dan kerja sama tim.</p>
            <p>Setiap minggu, santri mengikuti latihan pramuka yang meliputi berbagai kegiatan seperti hiking, camping, dan berbagai permainan edukatif.</p>
            <p>Melalui kegiatan pramuka, santri belajar untuk mandiri, bertanggung jawab, dan memiliki jiwa sosial yang tinggi.</p>''',
            
            '''<p>Pondok Pesantren membuka pendaftaran santri baru untuk tahun ajaran 2024. Pendaftaran dibuka untuk berbagai jenjang pendidikan mulai dari SD, SMP, hingga SMA.</p>
            <p>Calon santri dapat mendaftar melalui website resmi pondok pesantren atau datang langsung ke kantor pendaftaran. Persyaratan dan informasi lengkap dapat dilihat di website.</p>
            <p>Kami mengundang para orang tua untuk mendaftarkan putra-putrinya menjadi bagian dari keluarga besar pondok pesantren kami.</p>''',
            
            '''<p>Kegiatan outbound santri di Gunung Lawu berlangsung dengan sukses. Kegiatan ini diikuti oleh 50 santri yang terpilih berdasarkan prestasi dan kedisiplinan.</p>
            <p>Selama 3 hari 2 malam, santri melakukan berbagai aktivitas seperti hiking, camping, dan team building. Kegiatan ini bertujuan untuk melatih kemandirian dan kerja sama tim.</p>
            <p>Semua santri sangat antusias mengikuti kegiatan ini dan berharap kegiatan serupa dapat diadakan kembali di masa depan.</p>''',
            
            '''<p>Prestasi membanggakan diraih oleh santri kami dalam olimpiade matematika tingkat provinsi. Tiga santri berhasil meraih medali emas, perak, dan perunggu.</p>
            <p>Prestasi ini tidak lepas dari kerja keras dan dedikasi santri dalam belajar matematika. Ustadz pembimbing juga memberikan bimbingan intensif sebelum lomba.</p>
            <p>Kami berharap prestasi ini dapat memotivasi santri lainnya untuk terus belajar dan berprestasi.</p>''',
            
            '''<p>Program tahfidz Al-Quran menjadi salah satu program unggulan di pondok pesantren kami. Program ini diikuti oleh santri yang memiliki minat dan kemampuan menghafal Al-Quran.</p>
            <p>Setiap santri dibimbing oleh ustadz khusus yang memiliki sanad hafalan. Santri diwajibkan untuk menghafal minimal 1 juz per bulan.</p>
            <p>Program ini telah menghasilkan banyak hafidz dan hafidzah yang menjadi kebanggaan pondok pesantren.</p>''',
            
            '''<p>Kegiatan bakti sosial santri ke panti asuhan berlangsung dengan penuh kehangatan. Santri membagikan bantuan berupa sembako, pakaian, dan mainan untuk anak-anak panti asuhan.</p>
            <p>Kegiatan ini diikuti oleh 30 santri yang terpilih. Selain memberikan bantuan, santri juga mengadakan berbagai permainan dan kegiatan edukatif bersama anak-anak panti asuhan.</p>
            <p>Kegiatan ini mengajarkan santri untuk peduli terhadap sesama dan memiliki jiwa sosial yang tinggi.</p>''',
            
            '''<p>Peringatan Maulid Nabi Muhammad SAW diadakan dengan meriah. Acara ini diikuti oleh seluruh santri, ustadz/ustadzah, dan wali santri.</p>
            <p>Acara dimulai dengan pembacaan sholawat, dilanjutkan dengan ceramah agama tentang sejarah kelahiran Nabi Muhammad SAW, dan ditutup dengan doa bersama.</p>
            <p>Peringatan ini menjadi momen penting untuk mengingat kembali perjuangan dan teladan Nabi Muhammad SAW dalam kehidupan sehari-hari.</p>''',
        ]
        
        for i in range(count):
            title = titles[i % len(titles)] if i < len(titles) else f'Artikel Blog {i+1}'
            content = contents[i % len(contents)] if i < len(contents) else f'<p>Ini adalah konten artikel blog ke-{i+1}. Artikel ini membahas tentang berbagai kegiatan dan informasi terkini di pondok pesantren.</p>'
            
            # Random date dalam 6 bulan terakhir
            days_ago = random.randint(0, 180)
            published_date = timezone.now() - timedelta(days=days_ago)
            
            # Buat slug yang unik
            base_slug = slugify(title)
            slug = f'{base_slug}-{i+1}-{random.randint(1000, 9999)}'
            # Pastikan slug benar-benar unik
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{i+1}-{random.randint(1000, 9999)}'
            
            # Generate featured image
            featured_image_file = self.generate_dummy_image(
                title,
                width=1200,
                height=600,
                text_color=(30, 30, 30)
            )
            
            post = BlogPost.objects.create(
                title=title,
                slug=slug,
                author=author,
                content=content,
                excerpt=self._strip_html(content[:200]) + '...' if len(content) > 200 else self._strip_html(content),
                category=random.choice(categories) if categories else None,
                status=random.choice(['draft', 'published', 'published']),  # Lebih banyak published
                published_at=published_date if random.choice([True, True, True, False]) else None,
                is_featured=random.choice([True, False, False, False]),
                views_count=random.randint(0, 1000),
                likes_count=random.randint(0, 100),
                shares_count=random.randint(0, 50),
                meta_title=title,
                meta_description=self._strip_html(content[:200]) if len(content) > 200 else self._strip_html(content),
                meta_keywords='pondok pesantren, santri, pendidikan islam, kegiatan',
            )
            
            # Save featured image setelah object dibuat
            post.featured_image.save(f'blog_featured_{i+1}_{random.randint(1000, 9999)}.jpg', featured_image_file, save=False)
            post.save()
            
            # Add random tags
            if tags:
                num_tags = random.randint(1, 4)
                selected_tags = random.sample(tags, min(num_tags, len(tags)))
                post.tags.set(selected_tags)
            
            # Generate 1-3 additional images untuk blog post
            num_images = random.randint(1, 3)
            for img_idx in range(num_images):
                image_file = self.generate_dummy_image(
                    f'{title}\nGambar {img_idx + 1}',
                    width=800,
                    height=600,
                    text_color=(40, 40, 40)
                )
                
                blog_image = BlogImage.objects.create(
                    blog_post=post,
                    alt_text=f'{title} - Gambar {img_idx + 1}',
                    caption=f'Gambar ilustrasi untuk artikel: {title}',
                    order=img_idx + 1
                )
                blog_image.image.save(f'blog_image_{i+1}_{img_idx+1}_{random.randint(1000, 9999)}.jpg', image_file, save=False)
                blog_image.save()
            
            if (i + 1) % 5 == 0:
                self.stdout.write(f'  [OK] {i + 1} artikel dibuat dengan gambar...')

    def create_testimoni(self, count):
        """Membuat testimoni"""
        names = [
            'Ahmad Fauzi', 'Siti Nurhaliza', 'Muhammad Rizki', 'Fatimah Azzahra',
            'Abdullah Hadi', 'Aisyah Putri', 'Umar Faruq', 'Khadijah Salsabila',
            'Ali Akbar', 'Maryam Zahra', 'Hasan Basri', 'Zainab Firdaus',
            'Husain Al-Farisi', 'Aminah Khairunnisa', 'Ibrahim Al-Mustafa',
            'Rahmah Lutfiah', 'Yusuf Al-Hakim', 'Hajar Al-Munawwarah',
            'Ismail Al-Mubarak', 'Safiyah Al-Karimah'
        ]
        
        jabatans = [
            'Alumni 2020', 'Alumni 2019', 'Alumni 2021', 'Alumni 2018',
            'Alumni 2022', 'Wali Santri', 'Alumni 2017', 'Alumni 2023',
            'Alumni 2016', 'Wali Santri', 'Alumni 2015', 'Alumni 2024',
            'Wali Santri', 'Alumni 2014', 'Alumni 2013',
            'Wali Santri', 'Alumni 2012', 'Alumni 2011',
            'Wali Santri', 'Alumni 2010'
        ]
        
        testimonials = [
            'Pondok pesantren ini memberikan pendidikan yang sangat baik. Anak saya menjadi lebih disiplin dan rajin belajar. Terima kasih kepada semua ustadz dan ustadzah yang telah membimbing.',
            'Saya sangat puas dengan pendidikan di pondok ini. Anak saya tidak hanya pintar dalam pelajaran agama, tapi juga dalam pelajaran umum. Prestasinya meningkat drastis.',
            'Sebagai alumni, saya sangat bangga dengan pondok pesantren ini. Pendidikan yang saya dapatkan sangat bermanfaat untuk kehidupan saya sekarang.',
            'Pondok pesantren ini memiliki lingkungan yang sangat kondusif untuk belajar. Anak saya betah dan semangat belajar setiap hari.',
            'Saya merekomendasikan pondok pesantren ini untuk semua orang tua yang ingin memberikan pendidikan terbaik untuk anaknya.',
            'Pendidikan karakter di pondok ini sangat baik. Anak saya menjadi lebih sopan, disiplin, dan bertanggung jawab.',
            'Sebagai wali santri, saya sangat senang melihat perkembangan anak saya. Dia menjadi lebih mandiri dan percaya diri.',
            'Pondok pesantren ini tidak hanya mengajarkan ilmu agama, tapi juga ilmu umum. Anak saya mendapatkan pendidikan yang seimbang.',
            'Saya sangat berterima kasih kepada semua ustadz dan ustadzah yang telah membimbing anak saya dengan sabar dan telaten.',
            'Pondok pesantren ini memiliki fasilitas yang lengkap dan modern. Anak saya sangat nyaman belajar di sini.',
            'Sebagai alumni, saya merasa sangat beruntung pernah belajar di pondok pesantren ini. Ilmu yang saya dapatkan sangat bermanfaat.',
            'Pendidikan di pondok ini sangat berkualitas. Anak saya tidak hanya pintar, tapi juga memiliki akhlak yang baik.',
            'Saya sangat puas dengan pelayanan dan pendidikan di pondok pesantren ini. Semua staf sangat ramah dan profesional.',
            'Pondok pesantren ini memiliki program yang sangat menarik. Anak saya sangat antusias mengikuti semua kegiatan.',
            'Sebagai wali santri, saya sangat senang melihat anak saya berkembang dengan baik di pondok pesantren ini.',
            'Pendidikan agama di pondok ini sangat kuat. Anak saya menjadi lebih rajin sholat dan mengaji.',
            'Saya merekomendasikan pondok pesantren ini untuk semua orang. Pendidikan yang diberikan sangat berkualitas.',
            'Sebagai alumni, saya sangat bangga dengan prestasi pondok pesantren ini. Semoga terus berkembang dan maju.',
            'Pondok pesantren ini memiliki lingkungan yang sangat nyaman dan kondusif untuk belajar. Anak saya sangat betah.',
            'Saya sangat berterima kasih kepada semua pihak yang telah memberikan pendidikan terbaik untuk anak saya.',
        ]
        
        for i in range(count):
            name = names[i % len(names)] if i < len(names) else f'Testimoni {i+1}'
            jabatan = jabatans[i % len(jabatans)] if i < len(jabatans) else 'Alumni'
            testimoni = testimonials[i % len(testimonials)] if i < len(testimonials) else f'Testimoni ke-{i+1} tentang pondok pesantren ini.'
            
            days_ago = random.randint(0, 365)
            created_date = timezone.now() - timedelta(days=days_ago)
            
            Testimoni.objects.create(
                nama=name,
                jabatan=jabatan,
                testimoni=testimoni,
                rating=random.choice([4, 5, 5, 5, 5]),  # Lebih banyak rating 5
                is_published=random.choice([True, True, True, False]),
                order=i+1,
                created_at=created_date,
            )
            
            if (i + 1) % 5 == 0:
                self.stdout.write(f'  [OK] {i + 1} testimoni dibuat...')

    def create_pengumuman(self, count):
        """Membuat pengumuman"""
        juduls = [
            'Pengumuman Penerimaan Santri Baru Tahun Ajaran 2024',
            'Pengumuman Libur Hari Raya Idul Fitri 1445 H',
            'Pengumuman Kegiatan Muhadhoroh Bulan Ini',
            'Pengumuman Hasil Seleksi Santri Baru',
            'Pengumuman Kegiatan Outbound Santri',
            'Pengumuman Libur Semester Ganjil',
            'Pengumuman Kegiatan Bakti Sosial',
            'Pengumuman Peringatan Maulid Nabi',
            'Pengumuman Kegiatan Ekstrakurikuler',
            'Pengumuman Ujian Tengah Semester',
            'Pengumuman Kegiatan Tahfidz Al-Quran',
            'Pengumuman Libur Hari Raya Idul Adha',
            'Pengumuman Kegiatan Kajian Kitab',
            'Pengumuman Penerimaan Santri Baru Gelombang 2',
            'Pengumuman Kegiatan Pramuka',
            'Pengumuman Libur Akhir Semester',
            'Pengumuman Kegiatan Kaligrafi',
            'Pengumuman Hasil Ujian Semester',
            'Pengumuman Kegiatan Pencak Silat',
            'Pengumuman Libur Tahun Baru Hijriyah',
        ]
        
        kontens = [
            '''<p>Dengan hormat, kami sampaikan bahwa Pondok Pesantren membuka pendaftaran santri baru untuk tahun ajaran 2024/2025.</p>
            <p><strong>Persyaratan:</strong></p>
            <ul>
                <li>Usia minimal 7 tahun untuk jenjang SD</li>
                <li>Membawa fotocopy akta kelahiran</li>
                <li>Membawa fotocopy KTP orang tua</li>
                <li>Membawa pas foto 3x4 sebanyak 2 lembar</li>
            </ul>
            <p>Pendaftaran dibuka mulai tanggal 1 Januari 2024. Untuk informasi lebih lanjut, silakan hubungi panitia pendaftaran.</p>''',
            
            '''<p>Dengan hormat, kami sampaikan bahwa Pondok Pesantren akan libur dalam rangka menyambut Hari Raya Idul Fitri 1445 H.</p>
            <p><strong>Jadwal Libur:</strong></p>
            <ul>
                <li>Mulai: 8 April 2024</li>
                <li>Selesai: 15 April 2024</li>
                <li>Masuk kembali: 16 April 2024</li>
            </ul>
            <p>Selama libur, santri diharapkan tetap menjaga ibadah dan tidak lupa mengaji. Selamat Hari Raya Idul Fitri, mohon maaf lahir dan batin.</p>''',
            
            '''<p>Kepada seluruh santri, kami mengundang untuk mengikuti kegiatan Muhadhoroh (Latihan Pidato) yang akan dilaksanakan:</p>
            <p><strong>Waktu:</strong> Setiap Sabtu malam<br>
            <strong>Tempat:</strong> Aula Pondok Pesantren<br>
            <strong>Peserta:</strong> Semua santri</p>
            <p>Kegiatan ini bertujuan untuk melatih kemampuan public speaking santri. Diharapkan semua santri dapat mengikuti dengan baik.</p>''',
            
            '''<p>Dengan hormat, kami sampaikan hasil seleksi santri baru tahun ajaran 2024/2025.</p>
            <p>Hasil seleksi dapat dilihat di papan pengumuman atau melalui website resmi pondok pesantren.</p>
            <p>Bagi yang dinyatakan lulus, diharapkan segera melakukan daftar ulang sesuai jadwal yang telah ditentukan.</p>
            <p>Selamat kepada santri yang dinyatakan lulus. Bagi yang belum lulus, jangan berkecil hati dan tetap semangat.</p>''',
            
            '''<p>Kepada seluruh santri, kami mengundang untuk mengikuti kegiatan outbound yang akan dilaksanakan:</p>
            <p><strong>Waktu:</strong> 15-17 Maret 2024<br>
            <strong>Tempat:</strong> Gunung Lawu<br>
            <strong>Biaya:</strong> Rp 500.000 per santri</p>
            <p>Kegiatan ini bertujuan untuk melatih kemandirian dan kerja sama tim. Diharapkan semua santri dapat mengikuti.</p>''',
        ]
        
        for i in range(count):
            judul = juduls[i % len(juduls)] if i < len(juduls) else f'Pengumuman {i+1}'
            konten = kontens[i % len(kontens)] if i < len(kontens) else f'<p>Ini adalah konten pengumuman ke-{i+1}. Pengumuman ini berisi informasi penting untuk seluruh santri dan wali santri.</p>'
            
            days_ago = random.randint(0, 90)
            published_date = timezone.now() - timedelta(days=days_ago)
            
            # Buat slug yang unik
            base_slug = slugify(judul)
            slug = f'{base_slug}-{i+1}-{random.randint(1000, 9999)}'
            # Pastikan slug benar-benar unik
            while Pengumuman.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{i+1}-{random.randint(1000, 9999)}'
            
            Pengumuman.objects.create(
                judul=judul,
                slug=slug,
                konten=konten,
                status=random.choice(['draft', 'published', 'published']),
                is_penting=random.choice([True, False, False, False]),
                published_at=published_date if random.choice([True, True, True, False]) else None,
                meta_title=judul,
                meta_description=self._strip_html(konten[:200]) if len(konten) > 200 else self._strip_html(konten),
                created_at=published_date,
            )
            
            if (i + 1) % 5 == 0:
                self.stdout.write(f'  [OK] {i + 1} pengumuman dibuat...')

