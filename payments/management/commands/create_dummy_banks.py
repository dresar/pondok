"""
Management command untuk membuat data dummy BankAccount
"""
from django.core.management.base import BaseCommand
from payments.models import BankAccount


class Command(BaseCommand):
    help = 'Membuat data dummy untuk BankAccount'

    def handle(self, *args, **options):
        banks_data = [
            {
                'nama_bank': 'BCA',
                'nomor_rekening': '1234567890',
                'nama_pemilik_rekening': 'Pondok Pesantren Al-Hikmah',
                'biaya_pendaftaran': 500000,
                'is_active': True,
                'order': 1,
                'keterangan': 'Rekening utama untuk pembayaran pendaftaran'
            },
            {
                'nama_bank': 'BNI',
                'nomor_rekening': '9876543210',
                'nama_pemilik_rekening': 'Pondok Pesantren Al-Hikmah',
                'biaya_pendaftaran': 500000,
                'is_active': True,
                'order': 2,
                'keterangan': 'Rekening alternatif untuk pembayaran pendaftaran'
            },
            {
                'nama_bank': 'BRI',
                'nomor_rekening': '1122334455',
                'nama_pemilik_rekening': 'Pondok Pesantren Al-Hikmah',
                'biaya_pendaftaran': 500000,
                'is_active': True,
                'order': 3,
                'keterangan': 'Rekening alternatif untuk pembayaran pendaftaran'
            },
            {
                'nama_bank': 'Mandiri',
                'nomor_rekening': '5566778899',
                'nama_pemilik_rekening': 'Pondok Pesantren Al-Hikmah',
                'biaya_pendaftaran': 500000,
                'is_active': True,
                'order': 4,
                'keterangan': 'Rekening alternatif untuk pembayaran pendaftaran'
            },
            {
                'nama_bank': 'BSI',
                'nomor_rekening': '6677889900',
                'nama_pemilik_rekening': 'Pondok Pesantren Al-Hikmah',
                'biaya_pendaftaran': 500000,
                'is_active': True,
                'order': 5,
                'keterangan': 'Rekening syariah untuk pembayaran pendaftaran'
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for bank_data in banks_data:
            bank, created = BankAccount.objects.get_or_create(
                nomor_rekening=bank_data['nomor_rekening'],
                defaults=bank_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'[OK] Berhasil membuat rekening: {bank.get_display_name()} - {bank.nomor_rekening}'
                    )
                )
            else:
                # Update jika sudah ada
                for key, value in bank_data.items():
                    setattr(bank, key, value)
                bank.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'[UPDATE] Rekening sudah ada, diupdate: {bank.get_display_name()} - {bank.nomor_rekening}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n[OK] Selesai! Dibuat: {created_count}, Diupdate: {updated_count}'
            )
        )

