#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# IMPORTANT: Import psb_pondok SEBELUM Django setup
# Ini memastikan PyMySQL dikonfigurasi sebelum Django mencoba mengakses database
import psb_pondok  # noqa: F401

def main():
    """Run administrative tasks."""
    # Auto-detect production environment
    # Cek beberapa kondisi untuk menentukan apakah di production:
    # 1. Environment variable ENVIRONMENT=production
    # 2. Path mengandung 'public_html' (cPanel production path)
    # 3. Environment variable DJANGO_SETTINGS_MODULE sudah di-set ke settings_production
    # 4. File .env.production ada (opsional)
    env_environment = os.environ.get('ENVIRONMENT', '').lower()
    current_path = os.path.abspath(__file__)
    django_settings = os.environ.get('DJANGO_SETTINGS_MODULE', '')
    
    is_production = (
        env_environment == 'production' or 
        'public_html' in current_path or
        django_settings.endswith('settings_production') or
        os.path.exists(os.path.join(os.path.dirname(current_path), '.env.production'))
    )
    
    # Gunakan settings_production jika di production, otherwise settings (development)
    if is_production:
        default_settings = 'psb_pondok.settings_production'
    else:
        default_settings = 'psb_pondok.settings'
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', default_settings)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
