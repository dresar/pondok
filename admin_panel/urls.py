"""
URL Configuration untuk Admin Panel
Struktur URL yang rapi dan modular dengan support HTMX
"""
from django.urls import path, include
from . import views

app_name = 'admin-panel'

urlpatterns = [
    # Admin Panel Index
    path('', views.index, name='index'),
    
    # Santri URLs
    path('santri/', views.santri_list, name='santri_list'),
    path('santri/add/', views.santri_create, name='santri_create'),
    path('santri/<int:santri_id>/', views.santri_detail, name='santri_detail'),
    path('santri/<int:santri_id>/pdf/', views.santri_pdf, name='santri_pdf'),
    path('santri/<int:santri_id>/edit/', views.santri_update, name='santri_update'),
    path('santri/<int:santri_id>/delete/', views.santri_delete, name='santri_delete'),
    path('santri/<int:santri_id>/update-status/', views.update_santri_status, name='santri_update_status'),
    path('santri/export/', views.santri_export, name='santri_export'),
    path('santri/import/', views.santri_import, name='santri_import'),
    path('santri/bulk-action/', views.santri_bulk_action, name='santri_bulk_action'),
    path('santri/dokumen/', views.santri_dokumen_list, name='santri_dokumen_list'),
    path('santri/<int:santri_id>/approve-dokumen/', views.santri_approve_dokumen, name='santri_approve_dokumen'),
    
    # Keuangan URLs
    path('keuangan/', views.keuangan_dashboard, name='keuangan_dashboard'),
    path('keuangan/bank/', views.bank_account_list, name='bank_account_list'),
    path('keuangan/bank/<int:bank_id>/delete/', views.bank_account_delete, name='bank_account_delete'),
    
    # Payment URLs
    path('pembayaran/', views.payment_list, name='payment_list'),
    path('pembayaran/<int:payment_id>/', views.payment_detail, name='payment_detail'),
    path('pembayaran/<int:payment_id>/verify/', views.payment_verify, name='payment_verify'),
    path('pembayaran/export/', views.payment_export, name='payment_export'),
    path('pembayaran/bulk-action/', views.payment_bulk_action, name='payment_bulk_action'),
    
    # Alias untuk payment (backward compatibility)
    path('payment/', views.payment_list, name='payment_list_alias'),
    path('payment/<int:payment_id>/', views.payment_detail, name='payment_detail_alias'),
    path('payment/<int:payment_id>/verify/', views.payment_verify, name='payment_verify_alias'),
    
    # Website Settings (Hanya Superadmin)
    path('settings/', views.settings_view, name='settings'),
    path('settings/users/', views.user_settings_view, name='user_settings'),
    
    # User Profile
    path('profile/', views.user_profile, name='user_profile'),
    
    # User Account Management (Hanya Superuser)
    path('santri/user-accounts/', views.user_account_list, name='user_account_list'),
    path('santri/user-accounts/create/', views.user_account_create, name='user_account_create'),
    path('santri/user-accounts/<int:user_id>/edit/', views.user_account_update, name='user_account_update'),
    path('santri/user-accounts/<int:user_id>/delete/', views.user_account_delete, name='user_account_delete'),
    path('santri/user-accounts/<int:user_id>/change-password/', views.user_account_change_password, name='user_account_change_password'),
    
    # JSON endpoint untuk mengambil data Santri
    path('santri/<int:santri_id>/json/', views.santri_json_detail, name='santri_json_detail'),
    path('santri/search/', views.santri_search_api, name='santri_search_api'),
    
    # Staff Management (Role & Staff)
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/create/', views.staff_create, name='staff_create'),
    path('staff/<int:staff_id>/edit/', views.staff_update, name='staff_update'),
    path('staff/<int:staff_id>/delete/', views.staff_delete, name='staff_delete'),
    path('staff/<int:staff_id>/change-password/', views.staff_change_password, name='staff_change_password'),
    
    # Tenaga Pengajar Management
    path('tenaga-pengajar/bagian/', views.bagian_jabatan_list, name='bagian_jabatan_list'),
    path('tenaga-pengajar/bagian/<int:bagian_id>/delete/', views.bagian_jabatan_delete, name='bagian_jabatan_delete'),
    path('tenaga-pengajar/', views.tenaga_pengajar_list, name='tenaga_pengajar_list'),
    path('tenaga-pengajar/add/', views.tenaga_pengajar_create, name='tenaga_pengajar_create'),
    path('tenaga-pengajar/<int:pengajar_id>/', views.tenaga_pengajar_detail, name='tenaga_pengajar_detail'),
    path('tenaga-pengajar/<int:pengajar_id>/edit/', views.tenaga_pengajar_update, name='tenaga_pengajar_update'),
    path('tenaga-pengajar/<int:pengajar_id>/delete/', views.tenaga_pengajar_delete, name='tenaga_pengajar_delete'),
    
    # Login Statistics
    path('login-statistics/', views.login_statistics, name='login_statistics'),
    
    # Tools
    path('tools/image-converter/', views.image_converter, name='image_converter'),
    path('tools/image-converter/<int:image_id>/save/', views.save_converted_image, name='save_converted_image'),
    path('tools/converted-images/', views.converted_image_list, name='converted_image_list'),
    path('tools/converted-images/search/', views.converted_image_search_api, name='converted_image_search_api'),
    path('tools/converted-images/<int:image_id>/json/', views.converted_image_detail_json, name='converted_image_detail_json'),
    path('tools/converted-images/<int:image_id>/delete/', views.converted_image_delete, name='converted_image_delete'),
    path('tools/media-files/', views.media_files_manager, name='media_files_manager'),
    path('tools/media-files/delete-unused/', views.delete_unused_files, name='delete_unused_files'),

    # Bug notes
    path('bug-notes/create/', views.bug_note_create, name='bug_note_create'),
    path('bug-notes/', views.bug_note_list, name='bug_note_list'),
    path('bug-notes/export/', views.bug_note_export, name='bug_note_export'),
]

