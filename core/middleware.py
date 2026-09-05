"""
Middleware untuk Maintenance Mode
"""
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.deprecation import MiddlewareMixin
from core.models import WebsiteSettings


class MaintenanceModeMiddleware(MiddlewareMixin):
    """
    Middleware untuk menampilkan halaman maintenance jika mode maintenance aktif
    """
    
    # URL yang diizinkan saat maintenance (admin panel tetap bisa diakses)
    EXEMPT_URLS = [
        '/admin/',
        '/admin-panel/',
        '/static/',
        '/media/',
        '/summernote/',
    ]
    
    def process_request(self, request):
        """Check jika maintenance mode aktif"""
        try:
            settings = WebsiteSettings.load()
            
            # Jika maintenance mode tidak aktif, lanjutkan
            if not settings.maintenance_mode:
                return None
            
            # Cek jika URL diizinkan (admin panel, static files, dll)
            path = request.path
            for exempt_url in self.EXEMPT_URLS:
                if path.startswith(exempt_url):
                    return None
            
            # Cek jika user sudah login dan staff (admin bisa akses)
            if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
                return None
            
            # Tampilkan halaman maintenance
            context = {
                'settings': settings,
                'maintenance_message': settings.maintenance_message or 'Website sedang dalam perawatan. Kami akan kembali segera.',
            }
            html = render_to_string('maintenance.html', context, request=request)
            return HttpResponse(html, status=503)  # 503 Service Unavailable
            
        except Exception:
            # Jika ada error, biarkan request berjalan normal
            return None

