from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('pendaftaran/', views.pendaftaran, name='pendaftaran'),
    path('pendaftaran/pdf/', views.pendaftaran_pdf, name='pendaftaran_pdf'),
    path('status/', views.status, name='status'),
    path('dokumen/', views.dokumen, name='dokumen'),
    path('dokumen/upload/<str:doc_type>/', views.dokumen_upload, name='dokumen_upload'),
    path('dokumen/download/<str:doc_type>/', views.dokumen_download, name='dokumen_download'),
    path('pembayaran/', views.pembayaran, name='pembayaran'),
    path('riwayat/', views.riwayat, name='riwayat'),
    path('notifikasi/', views.notifikasi, name='notifikasi'),
]

