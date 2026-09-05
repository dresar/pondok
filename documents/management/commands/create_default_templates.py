from django.core.management.base import BaseCommand
from documents.models import DocumentTemplate


class Command(BaseCommand):
    help = 'Create default document templates'

    def handle(self, *args, **kwargs):
        # Template 1: Form A.1 - Formulir Pendaftaran
        template_a1_html = """
<div style="text-align: center; margin-bottom: 20px;">
    <img src="{{kop_surat_url}}" style="width: 100%; max-height: 60px;" />
</div>

<table style="width: 100%; margin-bottom: 20px;">
    <tr>
        <td style="width: 60%; border-right: 1px solid #007a87; padding-right: 15px;">
            <div style="text-align: center; color: #007a87; border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 20px;">
                <div style="font-size: 16pt;">{{arabic_name}}</div>
                <div style="font-size: 14pt; font-weight: bold;">{{nama_pondok}}</div>
                <div style="font-size: 9pt; color: #555;">{{alamat_pondok}}</div>
            </div>
            <div style="margin-top: 20px;">
                <h1 style="font-size: 24pt; margin: 0; line-height: 1.2;">FORMULIR</h1>
                <h1 style="font-size: 24pt; margin: 0; line-height: 1.2;">PENDAFTARAN</h1>
                <h1 style="font-size: 24pt; margin: 0; line-height: 1.2;">SANTRI BARU</h1>
            </div>
        </td>
        <td style="width: 40%; padding-left: 15px; text-align: center;">
            <div style="border: 2px solid #000; width: 90px; height: 115px; margin: 0 auto 10px; padding: 5px; font-size: 8pt;">
                Tempel<br>Pasfoto 3x4
            </div>
            <table style="width: 100%; border-bottom: 1px solid #000; margin-bottom: 20px;">
                <tr>
                    <td style="border-right: 1px solid #000; padding-right: 5px; font-size: 9pt;">No. Pendaftaran</td>
                    <td style="padding-left: 5px; font-weight: bold; font-size: 9pt;">{{no_pendaftaran}}</td>
                </tr>
            </table>
            <div style="margin-top: 20px;">
                <img src="{{logo_url}}" style="width: 100px; height: auto;" />
                <div style="font-style: italic; margin-top: 15px; font-size: 9pt; color: #333;">
                    ISLAMI<br>TERPERCAYA<br>KOMPETITIF
                </div>
            </div>
        </td>
    </tr>
</table>

<div style="border: 1px solid #000; padding: 10px; margin-bottom: 30px;">
    <div style="margin-bottom: 8px;">
        <strong>NAMA :</strong> <span style="text-decoration: underline;">{{nama_lengkap}}</span>
    </div>
    <div>
        <strong>ALAMAT :</strong> <span style="text-decoration: underline;">{{alamat_lengkap}}</span>
    </div>
</div>

<div style="text-align: center; margin-bottom: 15px;">
    <strong style="font-size: 12pt;">PERSYARATAN</strong>
</div>

<table style="width: 100%;">
    <tr><td style="width: 30px;">1.</td><td>Formulir pendaftaran yang telah diisi lengkap</td><td style="width: 35px;"><div style="width: 20px; height: 20px; border: 1px solid #000;"></div></td></tr>
    <tr><td>2.</td><td>Surat kelulusan dari sekolah/madrasah</td><td><div style="width: 20px; height: 20px; border: 1px solid #000;"></div></td></tr>
    <tr><td>3.</td><td>Fotokopi SKHUN/ijazah terakhir 2 lembar</td><td><div style="width: 20px; height: 20px; border: 1px solid #000;"></div></td></tr>
    <tr><td>4.</td><td>Pasfoto 3x4 4 lembar</td><td><div style="width: 20px; height: 20px; border: 1px solid #000;"></div></td></tr>
    <tr><td>5.</td><td>Fotokopi akta kelahiran 2 lembar</td><td><div style="width: 20px; height: 20px; border: 1px solid #000;"></div></td></tr>
    <tr><td>6.</td><td>Fotokopi kartu keluarga yang jelas 2 lembar</td><td><div style="width: 20px; height: 20px; border: 1px solid #000;"></div></td></tr>
    <tr><td>7.</td><td>Fotokopi KTP orang tua</td><td><div style="width: 20px; height: 20px; border: 1px solid #000;"></div></td></tr>
</table>
"""
        
        template_a1_css = """
@page {
    size: A4 portrait;
    margin: 1.5cm;
}
body {
    font-family: "Times New Roman", Times, serif;
    font-size: 11pt;
    color: #000;
}
table {
    border-collapse: collapse;
}
td {
    vertical-align: top;
    padding: 2px;
}
"""
        
        # Create or update template
        template_a1, created = DocumentTemplate.objects.update_or_create(
            slug='form-a1',
            defaults={
                'nama': 'Form A.1 - Formulir Pendaftaran',
                'deskripsi': 'Formulir cover pendaftaran santri baru dengan kop surat, logo, dan daftar persyaratan',
                'html_template': template_a1_html,
                'css_template': template_a1_css,
                'ukuran_kertas': 'A4',
                'orientasi': 'portrait',
                'is_active': True,
                'order': 1,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created template: {template_a1.nama}'))
        else:
            self.stdout.write(self.style.WARNING(f'Updated template: {template_a1.nama}'))
        
        self.stdout.write(self.style.SUCCESS('\nDefault templates created successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now customize templates via Admin Panel or Summernote editor.'))

