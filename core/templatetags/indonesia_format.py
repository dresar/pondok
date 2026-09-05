"""
Custom Template Filters untuk Format Indonesia
==============================================

Filter ini digunakan untuk format angka sesuai standar Indonesia:
- Titik (.) sebagai pemisah ribuan
- Contoh: 5000000 -> "Rp 5.000.000"

CATATAN PENTING:
- Setelah membuat atau mengubah file ini, RESTART SERVER DJANGO
- Django tidak akan mengenali template tag library baru tanpa restart
- Command: python manage.py runserver (stop dulu dengan Ctrl+C, lalu start lagi)
"""

from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter(name='rupiah')
def rupiah(value):
    """
    Format angka menjadi format Rupiah Indonesia dengan titik sebagai pemisah ribuan
    Contoh: 5000000 -> "Rp 5.000.000"
    
    Usage di template:
    {{ biaya.jumlah|rupiah }}
    """
    if value is None or value == '':
        return mark_safe('Rp 0')
    
    try:
        # Convert to int/float
        if isinstance(value, str):
            # Remove any existing formatting
            value = value.replace('.', '').replace(',', '')
            value = float(value)
        
        # Convert to int untuk menghilangkan desimal
        num = int(value)
        
        # Format dengan titik sebagai pemisah ribuan (format Indonesia)
        # Menggunakan format dengan koma dulu, lalu ganti dengan titik
        value_str = f"{num:,}".replace(',', '.')
        return mark_safe(f'Rp {value_str}')
    except (ValueError, TypeError, AttributeError):
        return mark_safe('Rp 0')

@register.filter(name='format_indonesia')
def format_indonesia(value, decimal_places=0):
    """
    Format angka menjadi format Indonesia dengan titik sebagai pemisah ribuan
    Contoh: 5000000 -> "5.000.000"
    
    Usage di template:
    {{ jumlah|format_indonesia }}
    {{ jumlah|format_indonesia:2 }}  # dengan 2 desimal
    """
    if value is None or value == '':
        return mark_safe('0')
    
    try:
        # Convert to float
        if isinstance(value, str):
            value = value.replace('.', '').replace(',', '')
            value = float(value)
        
        # Format dengan titik sebagai pemisah ribuan
        if decimal_places > 0:
            # Untuk desimal, format dengan koma sebagai desimal separator
            value_str = f"{value:,.{decimal_places}f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            # Untuk integer, hanya ganti koma dengan titik
            value_str = f"{int(value):,}".replace(',', '.')
        
        return mark_safe(value_str)
    except (ValueError, TypeError, AttributeError):
        return mark_safe('0')

@register.filter(name='tojson')
def tojson(value):
    """
    Convert value to JSON string (safe for use in JavaScript)
    Contoh: "Hello" -> "\"Hello\""
    
    Usage di template:
    {{ value|tojson }}
    {{ p.judul|escapejs|tojson }}
    """
    try:
        # Convert to JSON string
        json_str = json.dumps(value, ensure_ascii=False)
        return mark_safe(json_str)
    except (TypeError, ValueError):
        # Jika tidak bisa di-convert, return sebagai string yang di-escape
        try:
            return mark_safe(json.dumps(str(value), ensure_ascii=False))
        except:
            return mark_safe('""')
