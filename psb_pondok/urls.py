"""
URL configuration for psb_pondok project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve as static_serve
from django.http import HttpResponse
import os
import re
import admin_panel.views

# Serve static and media files
# Development: Django serve static & media; Production: handled by WhiteNoise/Apache
# Fallback: Jika Apache tidak bisa serve, Django akan serve sebagai fallback
urlpatterns = []

# Development mode: Django serve langsung
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production mode: Fallback untuk media files jika Apache tidak bisa serve
    # Static files di-handle oleh WhiteNoise/Apache, tapi media files perlu fallback
    # Gunakan Django's static_serve sebagai fallback dengan MIME type yang benar
    urlpatterns += [
        re_path(
            r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
            static_serve,
            {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': False,
            }
        ),
    ]

# URL patterns lainnya
urlpatterns += [
    # Favicon root (http://127.0.0.1:8000/favicon.ico) redirect ke static/favicon.ico
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico', permanent=True)),
    # Handle .well-known paths (untuk browser requests seperti traffic-advice, dll)
    # Mengembalikan 404 dengan response kosong untuk menghindari log warning
    re_path(r'^\.well-known/.*$', lambda request: HttpResponse(status=404, content_type='text/plain')),
    # Blokir Django admin bawaan di /admin/ dan arahkan ke admin-panel kustom
    # (menghindari ekspos URL admin default demi keamanan)
    path('admin/', RedirectView.as_view(url='/admin-panel/', permanent=True)),
    # Public URLs
    path('', include('core.urls_public')),
    # User URLs
    path('users/', include('users.urls')),
    # Admissions & Payments - sementara non-aktifkan untuk public
    # path('admissions/', include('admissions.urls')),  # Non-aktifkan
    # path('payments/', include('payments.urls')),  # Non-aktifkan
    path('admin-panel/', include('admin_panel.urls')),
    # Blog URLs - include langsung di root untuk namespace yang benar
    path('admin-panel/blog/', include('blog.urls')),
    # Core URLs (FAQ, Program)
    path('admin-panel/core/', include('core.urls')),
    # Documents URLs (PDF Generator)
    path('admin-panel/documents/', include('documents.urls')),
    # Summernote URLs
    path('summernote/', include('django_summernote.urls')),
    # CDN URLs (Public access untuk gambar)
    path('cdn/image/<int:image_id>/', admin_panel.views.cdn_image_view, name='cdn_image'),
]

# Custom error handlers (used when DEBUG=False)
handler404 = 'core.views_public.error_404'
handler500 = 'core.views_public.error_500'
handler403 = 'core.views_public.error_403'
handler400 = 'core.views_public.error_400'
