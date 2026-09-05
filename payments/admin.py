from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['santri', 'bank_pengirim', 'jumlah_transfer', 'status', 'created_at']
    list_filter = ['status', 'bank_pengirim', 'created_at']
    search_fields = ['santri__nama_lengkap', 'santri__nisn', 'nama_pemilik_rekening']
    readonly_fields = ['created_at', 'updated_at', 'verified_at', 'verified_by']
    date_hierarchy = 'created_at'
