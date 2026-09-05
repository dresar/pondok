"""
Management command untuk membuat dummy data SEO untuk WebsiteSettings
"""
from django.core.management.base import BaseCommand
from core.models import WebsiteSettings


class Command(BaseCommand):
    help = 'Membuat dummy data SEO untuk Pondok Pesantren Modern Raudhatussalam Mahato'

    def handle(self, *args, **options):
        # Get or create WebsiteSettings (singleton)
        settings, created = WebsiteSettings.objects.get_or_create(pk=1)
        
        # Update SEO fields
        settings.meta_title = "Pondok Pesantren Modern Raudhatussalam Mahato - Pendidikan Islam Terpadu"
        settings.meta_description = "Pondok Pesantren Modern Raudhatussalam Mahato menyelenggarakan pendidikan Islam terpadu dengan kurikulum modern. Mencetak generasi unggul yang berkarakter Islami, cerdas, dan berakhlak mulia. Pendaftaran santri baru dibuka setiap tahun."
        settings.meta_keywords = "pondok pesantren modern, raudhatussalam mahato, pendidikan islam, pesantren modern, pendidikan terpadu, santri, pendidikan karakter, pendidikan islami, pesantren sumatera, pendidikan berkualitas, tahfidz quran, pendidikan agama, pendidikan umum, sekolah islam, boarding school"
        
        settings.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Dummy data SEO berhasil dibuat untuk: {settings.meta_title}'
            )
        )
        self.stdout.write(f'  Meta Description: {settings.meta_description[:80]}...')
        self.stdout.write(f'  Meta Keywords: {settings.meta_keywords[:80]}...')

