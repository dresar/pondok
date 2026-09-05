from django import forms
from .models import Santri


class SantriForm(forms.ModelForm):
    """Form untuk pendaftaran santri baru"""
    
    class Meta:
        model = Santri
        fields = [
            'nama_lengkap', 'nisn', 'tempat_lahir', 'tanggal_lahir', 'jenis_kelamin',
            'nama_ayah', 'nama_ibu', 'pekerjaan_ayah', 'pekerjaan_ibu',
            'alamat', 'no_hp', 'email',
            'asal_sekolah', 'kelas_terakhir'
        ]
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Masukkan nama lengkap'
            }),
            'nisn': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': '10 digit NISN',
                'maxlength': '10'
            }),
            'tempat_lahir': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Kota tempat lahir'
            }),
            'tanggal_lahir': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'date'
            }),
            'jenis_kelamin': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'nama_ayah': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Nama lengkap ayah'
            }),
            'nama_ibu': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Nama lengkap ibu'
            }),
            'pekerjaan_ayah': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Pekerjaan ayah (opsional)'
            }),
            'pekerjaan_ibu': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Pekerjaan ibu (opsional)'
            }),
            'alamat': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Alamat lengkap tempat tinggal'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': '08xxxxxxxxxx',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'email@example.com (opsional)'
            }),
            'asal_sekolah': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Nama sekolah asal'
            }),
            'kelas_terakhir': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Contoh: IX, XII, dll'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Menambahkan label yang lebih jelas
        self.fields['nama_lengkap'].label = 'Nama Lengkap'
        self.fields['nisn'].label = 'NISN'
        self.fields['tempat_lahir'].label = 'Tempat Lahir'
        self.fields['tanggal_lahir'].label = 'Tanggal Lahir'
        self.fields['jenis_kelamin'].label = 'Jenis Kelamin'
        self.fields['nama_ayah'].label = 'Nama Ayah'
        self.fields['nama_ibu'].label = 'Nama Ibu'
        self.fields['pekerjaan_ayah'].label = 'Pekerjaan Ayah (Opsional)'
        self.fields['pekerjaan_ibu'].label = 'Pekerjaan Ibu (Opsional)'
        self.fields['alamat'].label = 'Alamat Lengkap'
        self.fields['no_hp'].label = 'No. HP'
        self.fields['email'].label = 'Email (Opsional)'
        self.fields['asal_sekolah'].label = 'Asal Sekolah'
        self.fields['kelas_terakhir'].label = 'Kelas Terakhir'

