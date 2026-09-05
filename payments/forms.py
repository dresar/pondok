from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    """Form untuk upload bukti pembayaran"""
    
    class Meta:
        model = Payment
        fields = [
            'bank_pengirim', 'nama_pemilik_rekening', 'jumlah_transfer', 'bukti_transfer', 'catatan'
        ]
        widgets = {
            'bank_pengirim': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'nama_pemilik_rekening': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Nama sesuai rekening pengirim'
            }),
            'jumlah_transfer': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Jumlah yang ditransfer',
                'step': '0.01',
                'min': '0'
            }),
            'bukti_transfer': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'catatan': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Catatan tambahan (opsional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bank_pengirim'].label = 'Bank Pengirim'
        self.fields['nama_pemilik_rekening'].label = 'Nama Pemilik Rekening'
        self.fields['jumlah_transfer'].label = 'Jumlah Transfer (Rp)'
        self.fields['bukti_transfer'].label = 'Bukti Transfer (Foto/Scan)'
        self.fields['catatan'].label = 'Catatan (Opsional)'

