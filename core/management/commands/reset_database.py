"""
Management command untuk reset database dan membuat ulang data dummy
Usage: python manage.py reset_database
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Reset database (flush, migrate, dan buat ulang data dummy)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-dummy',
            action='store_true',
            help='Jangan membuat data dummy setelah reset',
        )
        parser.add_argument(
            '--no-migrate',
            action='store_true',
            help='Jangan menjalankan migrate (hanya flush)',
        )

    def handle(self, *args, **options):
        no_dummy = options.get('no_dummy', False)
        no_migrate = options.get('no_migrate', False)
        
        self.stdout.write(self.style.WARNING('=' * 60))
        self.stdout.write(self.style.WARNING('RESET DATABASE'))
        self.stdout.write(self.style.WARNING('=' * 60))
        self.stdout.write(self.style.ERROR('PERINGATAN: Semua data akan dihapus!'))
        
        # Konfirmasi
        confirm = input('Apakah Anda yakin ingin melanjutkan? (yes/no): ')
        if confirm.lower() != 'yes':
            self.stdout.write(self.style.ERROR('Dibatalkan.'))
            return
        
        # 1. Flush database
        self.stdout.write('\n[1/4] Menghapus semua data dari database...')
        try:
            call_command('flush', '--noinput')
            self.stdout.write(self.style.SUCCESS('  [OK] Database berhasil di-flush'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  [ERROR] Gagal flush: {e}'))
            return
        
        # 2. Migrate (jika tidak di-skip)
        if not no_migrate:
            self.stdout.write('\n[2/4] Menjalankan migrate...')
            try:
                call_command('migrate', '--noinput')
                self.stdout.write(self.style.SUCCESS('  [OK] Migrate berhasil'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [ERROR] Gagal migrate: {e}'))
                return
        else:
            self.stdout.write('\n[2/4] Migrate di-skip')
        
        # 3. Buat superuser (jika belum ada)
        self.stdout.write('\n[3/4] Membuat superuser...')
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@pondok.id',
                    password='admin123',
                    first_name='Administrator',
                    last_name='Pondok',
                )
                self.stdout.write(self.style.SUCCESS('  [OK] Superuser admin dibuat (password: admin123)'))
            else:
                self.stdout.write(self.style.WARNING('  - Superuser admin sudah ada'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  [ERROR] Gagal membuat superuser: {e}'))
        
        # 4. Buat data dummy (jika tidak di-skip)
        if not no_dummy:
            self.stdout.write('\n[4/4] Membuat data dummy...')
            try:
                call_command('create_all_dummy_data', '--clear')
                self.stdout.write(self.style.SUCCESS('  [OK] Data dummy berhasil dibuat'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [ERROR] Gagal membuat data dummy: {e}'))
        else:
            self.stdout.write('\n[4/4] Pembuatan data dummy di-skip')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('RESET DATABASE SELESAI!'))
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('\nAkun Login:'))
        self.stdout.write('  - Username: admin')
        self.stdout.write('  - Password: admin123')

