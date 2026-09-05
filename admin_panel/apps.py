from django.apps import AppConfig


class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'  # Nama module (bukan folder)
    verbose_name = 'Admin Panel'
