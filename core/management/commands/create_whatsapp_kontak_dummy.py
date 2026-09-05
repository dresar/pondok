"""
Management command untuk membuat data dummy lengkap untuk fitur WhatsApp & Kontak
Usage: python manage.py create_whatsapp_kontak_dummy [--clear]
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random

from core.models import (
    WhatsAppTemplateKategori, WhatsAppTemplate, ContactPerson, Kontak
)
from admissions.models import Santri


class Command(BaseCommand):
    help = 'Membuat data dummy lengkap untuk fitur WhatsApp & Kontak'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus semua data sebelum membuat data baru'
        )

    def handle(self, *args, **options):
        clear = options.get('clear', False)
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('MEMBUAT DATA DUMMY WHATSAPP & KONTAK'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        if clear:
            self.stdout.write(self.style.WARNING('Menghapus data lama...'))
            Kontak.objects.all().delete()
            WhatsAppTemplate.objects.all().delete()
            WhatsAppTemplateKategori.objects.all().delete()
            ContactPerson.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('  Data lama berhasil dihapus.'))
        
        # 1. WhatsAppTemplateKategori
        self.stdout.write('\n[1/4] Membuat WhatsAppTemplateKategori...')
        categories = self.create_whatsapp_categories()
        
        # 2. WhatsAppTemplate
        self.stdout.write('[2/4] Membuat WhatsAppTemplate...')
        self.create_whatsapp_templates(categories)
        
        # 3. ContactPerson
        self.stdout.write('[3/4] Membuat ContactPerson...')
        self.create_contact_persons()
        
        # 4. Kontak/Inquiry
        self.stdout.write('[4/4] Membuat Kontak/Inquiry...')
        self.create_kontak_inquiry()
        
        # Summary
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('SUMMARY DATA DUMMY WHATSAPP & KONTAK'))
        self.stdout.write('=' * 70)
        self.stdout.write(f'WhatsAppTemplateKategori: {WhatsAppTemplateKategori.objects.count()}')
        self.stdout.write(f'WhatsAppTemplate: {WhatsAppTemplate.objects.count()}')
        self.stdout.write(f'  - Public Templates: {WhatsAppTemplate.objects.filter(tipe="public").count()}')
        self.stdout.write(f'  - System Templates: {WhatsAppTemplate.objects.filter(tipe="system").count()}')
        self.stdout.write(f'ContactPerson: {ContactPerson.objects.count()}')
        self.stdout.write(f'Kontak/Inquiry: {Kontak.objects.count()}')
        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS('\nData dummy WhatsApp & Kontak berhasil dibuat!'))

    def create_whatsapp_categories(self):
        """Buat kategori template WhatsApp"""
        categories_data = [
            {
                'nama': 'Pendaftaran',
                'deskripsi': 'Template untuk notifikasi pendaftaran santri baru',
                'order': 1,
            },
            {
                'nama': 'Pembayaran',
                'deskripsi': 'Template untuk notifikasi pembayaran dan verifikasi',
                'order': 2,
            },
            {
                'nama': 'Pengumuman',
                'deskripsi': 'Template untuk pengumuman dan informasi penting',
                'order': 3,
            },
            {
                'nama': 'Reminder',
                'deskripsi': 'Template untuk pengingat dan follow-up',
                'order': 4,
            },
            {
                'nama': 'Selamat Datang',
                'deskripsi': 'Template untuk menyambut santri baru',
                'order': 5,
            },
            {
                'nama': 'Broadcast',
                'deskripsi': 'Template untuk broadcast massal',
                'order': 6,
            },
        ]
        
        categories = {}
        for data in categories_data:
            kategori, created = WhatsAppTemplateKategori.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            categories[data['nama']] = kategori
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [OK] Kategori: {data["nama"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Kategori: {data["nama"]} sudah ada'))
        
        return categories

    def create_whatsapp_templates(self, categories):
        """Buat template WhatsApp"""
        templates_data = [
            # Template Public (untuk website)
            {
                'nama': 'Konfirmasi Pendaftaran',
                'kategori': categories.get('Pendaftaran'),
                'tipe': 'public',
                'pesan': '''Assalamu\'alaikum {nama}

Terima kasih telah mendaftar di Pesantren Modern Raudhatussalam.

*Data Pendaftaran:*
📋 Nomor Pendaftaran: {nomor_pendaftaran}
📅 Tanggal Daftar: {tanggal_daftar}
👤 Nama: {nama_lengkap}
📧 Email: {email}
📱 No. HP: {no_hp}

*Status:* {status}

Silakan lengkapi dokumen dan lakukan pembayaran sesuai ketentuan.

Terima kasih,
Panitia Penerimaan Santri Baru
Pesantren Modern Raudhatussalam''',
                'variabel': 'nama, nomor_pendaftaran, tanggal_daftar, nama_lengkap, email, no_hp, status',
                'order': 1,
            },
            {
                'nama': 'Pengingat Pembayaran',
                'kategori': categories.get('Pembayaran'),
                'tipe': 'public',
                'pesan': '''Assalamu\'alaikum {nama}

*Pengingat Pembayaran*

Anda belum melakukan pembayaran untuk pendaftaran santri baru.

*Detail Pembayaran:*
💰 Biaya: Rp {biaya}
🏦 Rekening: {bank} - {no_rekening}
👤 A.n: {nama_pemilik_rekening}

*Cara Pembayaran:*
1. Transfer ke rekening di atas
2. Upload bukti transfer di website
3. Tunggu verifikasi (1-2 hari kerja)

*Batas Waktu:* {batas_waktu}

Terima kasih,
Panitia Penerimaan Santri Baru''',
                'variabel': 'nama, biaya, bank, no_rekening, nama_pemilik_rekening, batas_waktu',
                'order': 2,
            },
            {
                'nama': 'Pembayaran Terverifikasi',
                'kategori': categories.get('Pembayaran'),
                'tipe': 'public',
                'pesan': '''Assalamu\'alaikum {nama}

*Pembayaran Terverifikasi* ✅

Pembayaran Anda sebesar Rp {jumlah} telah terverifikasi.

*Status Pendaftaran:* {status}

Langkah selanjutnya:
1. Lengkapi dokumen yang diperlukan
2. Tunggu pengumuman hasil seleksi
3. Ikuti tes seleksi sesuai jadwal

Terima kasih,
Panitia Penerimaan Santri Baru''',
                'variabel': 'nama, jumlah, status',
                'order': 3,
            },
            {
                'nama': 'Selamat Datang Santri Baru',
                'kategori': categories.get('Selamat Datang'),
                'tipe': 'public',
                'pesan': '''Assalamu\'alaikum Warahmatullahi Wabarakatuh

Selamat datang di Pesantren Modern Raudhatussalam, {nama}! 🎉

Kami mengucapkan selamat karena Anda telah diterima sebagai santri baru tahun ajaran {tahun_ajaran}.

*Informasi Penting:*
📅 Tanggal Masuk: {tanggal_masuk}
📍 Lokasi: Pesantren Modern Raudhatussalam
📱 Contact Person: {contact_person}

*Persiapan:*
1. Siapkan dokumen yang diperlukan
2. Bawa perlengkapan sesuai ketentuan
3. Datang tepat waktu

Kami tunggu kehadiran Anda!

Barakallahu fiikum,
Panitia Penerimaan Santri Baru''',
                'variabel': 'nama, tahun_ajaran, tanggal_masuk, contact_person',
                'order': 4,
            },
            
            # Template System (untuk admin panel / broadcast)
            {
                'nama': 'Broadcast Pengumuman Penting',
                'kategori': categories.get('Broadcast'),
                'tipe': 'system',
                'pesan': '''*PENGUMUMAN PENTING* 📢

Assalamu\'alaikum {nama}

{isi_pengumuman}

*Tanggal:* {tanggal_hari_ini}
*Lokasi:* Pesantren Modern Raudhatussalam

Terima kasih atas perhatiannya.

Panitia Penerimaan Santri Baru
Pesantren Modern Raudhatussalam''',
                'variabel': 'nama, isi_pengumuman, tanggal_hari_ini',
                'order': 1,
            },
            {
                'nama': 'Reminder Lengkapi Dokumen',
                'kategori': categories.get('Reminder'),
                'tipe': 'system',
                'pesan': '''Assalamu\'alaikum {nama}

*Pengingat: Lengkapi Dokumen*

Anda belum melengkapi dokumen pendaftaran.

*Dokumen yang Belum Lengkap:*
{dokumen_belum_lengkap}

*Cara Upload:*
1. Login ke website pendaftaran
2. Upload dokumen di halaman profil
3. Tunggu verifikasi

*Batas Waktu:* {batas_waktu}

Terima kasih,
Panitia Penerimaan Santri Baru''',
                'variabel': 'nama, dokumen_belum_lengkap, batas_waktu',
                'order': 2,
            },
            {
                'nama': 'Jadwal Tes Seleksi',
                'kategori': categories.get('Pengumuman'),
                'tipe': 'system',
                'pesan': '''Assalamu\'alaikum {nama}

*JADWAL TES SELEKSI*

Anda diundang untuk mengikuti tes seleksi:

*Tanggal:* {tanggal_tes}
*Waktu:* {waktu_tes}
*Lokasi:* {lokasi_tes}

*Yang Harus Dibawa:*
1. Kartu pendaftaran
2. Alat tulis
3. Dokumen asli untuk verifikasi

*Catatan:* Datang 15 menit sebelum waktu tes.

Terima kasih,
Panitia Penerimaan Santri Baru''',
                'variabel': 'nama, tanggal_tes, waktu_tes, lokasi_tes',
                'order': 3,
            },
            {
                'nama': 'Hasil Seleksi',
                'kategori': categories.get('Pengumuman'),
                'tipe': 'system',
                'pesan': '''Assalamu\'alaikum {nama}

*HASIL SELEKSI*

Kami mengucapkan selamat karena Anda *{hasil_seleksi}* dalam seleksi santri baru.

*Detail:*
📋 Nomor Pendaftaran: {nomor_pendaftaran}
📅 Tanggal Pengumuman: {tanggal_hari_ini}
{detail_tambahan}

{langkah_selanjutnya}

Terima kasih,
Panitia Penerimaan Santri Baru''',
                'variabel': 'nama, hasil_seleksi, nomor_pendaftaran, tanggal_hari_ini, detail_tambahan, langkah_selanjutnya',
                'order': 4,
            },
            {
                'nama': 'Reminder Pembayaran SPP',
                'kategori': categories.get('Reminder'),
                'tipe': 'system',
                'pesan': '''Assalamu\'alaikum {nama}

*Pengingat Pembayaran SPP*

Pembayaran SPP bulan {bulan} belum dilakukan.

*Detail:*
💰 Jumlah: Rp {jumlah_spp}
📅 Jatuh Tempo: {jatuh_tempo}
🏦 Rekening: {bank} - {no_rekening}

*Cara Pembayaran:*
1. Transfer ke rekening di atas
2. Upload bukti transfer
3. Konfirmasi ke admin

Terima kasih,
Bendahara Pesantren''',
                'variabel': 'nama, bulan, jumlah_spp, jatuh_tempo, bank, no_rekening',
                'order': 5,
            },
            {
                'nama': 'Informasi Kegiatan',
                'kategori': categories.get('Pengumuman'),
                'tipe': 'system',
                'pesan': '''Assalamu\'alaikum {nama}

*INFORMASI KEGIATAN*

Kami mengundang Anda untuk mengikuti:

*Kegiatan:* {nama_kegiatan}
*Tanggal:* {tanggal_kegiatan}
*Waktu:* {waktu_kegiatan}
*Lokasi:* {lokasi_kegiatan}

*Deskripsi:*
{deskripsi_kegiatan}

*Catatan:* {catatan}

Kami tunggu kehadiran Anda!

Panitia Kegiatan
Pesantren Modern Raudhatussalam''',
                'variabel': 'nama, nama_kegiatan, tanggal_kegiatan, waktu_kegiatan, lokasi_kegiatan, deskripsi_kegiatan, catatan',
                'order': 6,
            },
            {
                'nama': 'Follow Up Pendaftaran',
                'kategori': categories.get('Reminder'),
                'tipe': 'system',
                'pesan': '''Assalamu\'alaikum {nama}

*Follow Up Pendaftaran*

Kami ingin memastikan proses pendaftaran Anda berjalan lancar.

*Status Saat Ini:*
{status_pendaftaran}

*Langkah Selanjutnya:*
{langkah_selanjutnya}

Jika ada pertanyaan, jangan ragu untuk menghubungi kami:
📱 {no_hp_contact}
📧 {email_contact}

Terima kasih,
Panitia Penerimaan Santri Baru''',
                'variabel': 'nama, status_pendaftaran, langkah_selanjutnya, no_hp_contact, email_contact',
                'order': 7,
            },
        ]
        
        created = 0
        for data in templates_data:
            template, created_flag = WhatsAppTemplate.objects.get_or_create(
                nama=data['nama'],
                tipe=data['tipe'],
                defaults=data
            )
            if created_flag:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  [OK] Template: {data["nama"]} ({data["tipe"]})'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Template: {data["nama"]} sudah ada'))
        
        self.stdout.write(self.style.SUCCESS(f'  Total: {created} template dibuat'))

    def create_contact_persons(self):
        """Buat Contact Person"""
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
            {
                'nama': 'Ustz. Siti Fatimah, S.Pd',
                'no_hp': '082345678901',
                'order': 3,
                'is_active': True,
            },
            {
                'nama': 'Ust. Ahmad Fauzi, S.Ag',
                'no_hp': '083456789012',
                'order': 4,
                'is_active': True,
            },
            {
                'nama': 'Ustz. Nur Aisyah, S.Pd.I',
                'no_hp': '084567890123',
                'order': 5,
                'is_active': False,  # Tidak aktif
            },
        ]
        
        created = 0
        for data in contact_data:
            contact, created_flag = ContactPerson.objects.get_or_create(
                nama=data['nama'],
                defaults=data
            )
            if created_flag:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'  [OK] Contact Person: {data["nama"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'  [-] Contact Person: {data["nama"]} sudah ada'))
        
        self.stdout.write(self.style.SUCCESS(f'  Total: {created} contact person dibuat'))

    def create_kontak_inquiry(self):
        """Buat Kontak/Inquiry dari website"""
        nama_list = [
            'Budi Santoso', 'Siti Nurhaliza', 'Ahmad Fauzi', 'Mariam Sari',
            'Rizki Pratama', 'Dewi Lestari', 'Hasan Maulana', 'Fatimah Zahra',
            'Muhammad Rizki', 'Aisyah Putri', 'Ali Rahman', 'Khadijah Dewi',
            'Husain Pratama', 'Zainab Sari', 'Umar Fauzi', 'Nur Aisyah'
        ]
        
        subjek_list = [
            'Pertanyaan tentang Pendaftaran Santri Baru',
            'Informasi Biaya Pendidikan',
            'Jadwal Kunjungan Orang Tua',
            'Fasilitas Pesantren',
            'Program Pendidikan yang Tersedia',
            'Persyaratan Pendaftaran',
            'Jadwal Tes Seleksi',
            'Informasi Beasiswa',
            'Kegiatan Ekstrakurikuler',
            'Fasilitas Asrama',
            'Sistem Pembelajaran',
            'Kurikulum Pesantren',
            'Pertanyaan tentang KMI',
            'Informasi Akreditasi',
            'Cara Daftar Online',
            'Kontak Panitia Pendaftaran',
        ]
        
        pesan_templates = [
            'Saya ingin bertanya tentang {subjek}. Mohon informasi lebih lanjut.',
            'Apakah masih ada kuota untuk pendaftaran tahun ajaran 2025/2026?',
            'Saya tertarik untuk mendaftarkan anak saya. Bagaimana caranya?',
            'Bisa tolong kirimkan informasi lengkap tentang {subjek}?',
            'Saya ingin mengetahui lebih detail tentang {subjek}. Terima kasih.',
            'Apakah ada program beasiswa untuk santri berprestasi?',
            'Kapan jadwal kunjungan orang tua? Saya ingin melihat fasilitas pesantren.',
            'Berapa biaya pendidikan per bulan? Apakah ada cicilan?',
        ]
        
        status_choices = ['baru', 'dibaca', 'dibalas', 'selesai']
        balasan_templates = [
            'Terima kasih telah menghubungi kami. Kami akan segera menindaklanjuti pertanyaan Anda.',
            'Terima kasih atas pertanyaannya. Informasi lengkap telah kami kirimkan via email.',
            'Kami telah menerima pertanyaan Anda. Tim kami akan menghubungi Anda segera.',
            'Terima kasih. Pertanyaan Anda sudah kami catat dan akan segera direspon.',
        ]
        
        created = 0
        for i in range(30):  # Buat 30 kontak/inquiry
            nama = random.choice(nama_list) + (f" {i+1}" if i > 15 else "")
            subjek = random.choice(subjek_list)
            pesan_template = random.choice(pesan_templates)
            pesan = pesan_template.replace('{subjek}', subjek.lower())
            
            # Generate email
            email = f"{nama.lower().replace(' ', '.')}@example.com"
            
            # Generate no HP
            no_hp = f"08{random.randint(100000000, 999999999)}"
            
            # Status dan balasan
            status = random.choice(status_choices)
            balasan = ''
            if status in ['dibalas', 'selesai']:
                balasan = random.choice(balasan_templates)
            
            # Generate tanggal (random dalam 30 hari terakhir)
            created_at = timezone.now() - timedelta(days=random.randint(0, 30))
            
            kontak = Kontak.objects.create(
                nama=nama,
                email=email,
                no_hp=no_hp,
                subjek=subjek,
                pesan=pesan,
                status=status,
                balasan=balasan,
            )
            # Update created_at manually
            Kontak.objects.filter(id=kontak.id).update(created_at=created_at)
            
            created += 1
            if created % 10 == 0:
                self.stdout.write(f'  [OK] {created}/30 kontak dibuat...')
        
        self.stdout.write(self.style.SUCCESS(f'  Total: {created} kontak/inquiry dibuat'))

