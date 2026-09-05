"""
URL Configuration untuk Core App
"""
from django.urls import path
from . import views, views_crud

app_name = 'core'

urlpatterns = [
    # Public URLs (redirected to login)
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # FAQ CRUD
    path('faq/', views_crud.faq_list, name='faq_list'),
    path('faq/add/', views_crud.faq_create, name='faq_create'),
    path('faq/<int:faq_id>/edit/', views_crud.faq_update, name='faq_update'),
    path('faq/<int:faq_id>/delete/', views_crud.faq_delete, name='faq_delete'),
    
    # Program CRUD
    path('program/', views_crud.program_list, name='program_list'),
    path('program/add/', views_crud.program_form, name='program_create'),
    path('program/<int:program_id>/edit/', views_crud.program_form, name='program_update'),
    path('program/<int:program_id>/delete/', views_crud.program_delete, name='program_delete'),
    
    # WhatsApp Template CRUD
    path('whatsapp-template/', views_crud.whatsapp_template_list, name='whatsapp_template_list'),
    path('whatsapp-template/add/', views_crud.whatsapp_template_form, name='whatsapp_template_create'),
    path('whatsapp-template/<int:template_id>/edit/', views_crud.whatsapp_template_form, name='whatsapp_template_update'),
    path('whatsapp-template/<int:template_id>/delete/', views_crud.whatsapp_template_delete, name='whatsapp_template_delete'),
    path('whatsapp-template/kategori/create/', views_crud.whatsapp_template_kategori_create, name='whatsapp_template_kategori_create'),
    
    # Kontak CRUD
    path('kontak/', views_crud.kontak_list, name='kontak_list'),
    path('kontak/<int:kontak_id>/', views_crud.kontak_form, name='kontak_detail'),
    path('kontak/<int:kontak_id>/edit/', views_crud.kontak_form, name='kontak_update'),
    path('kontak/<int:kontak_id>/delete/', views_crud.kontak_delete, name='kontak_delete'),
    
    # WhatsApp Broadcast
    path('whatsapp-broadcast/', views_crud.whatsapp_broadcast, name='whatsapp_broadcast'),
    
    # Website Settings CRUD
    path('hero-section/', views_crud.hero_section_list, name='hero_section_list'),
    path('hero-section/add/', views_crud.hero_section_form, name='hero_section_create'),
    path('hero-section/<int:hero_id>/edit/', views_crud.hero_section_form, name='hero_section_update'),
    path('hero-section/<int:hero_id>/delete/', views_crud.hero_section_delete, name='hero_section_delete'),
    
    path('sejarah-timeline/', views_crud.sejarah_timeline_list, name='sejarah_timeline_list'),
    path('sejarah-timeline/add/', views_crud.sejarah_timeline_form, name='sejarah_timeline_create'),
    path('sejarah-timeline/<int:timeline_id>/edit/', views_crud.sejarah_timeline_form, name='sejarah_timeline_update'),
    path('sejarah-timeline/<int:timeline_id>/delete/', views_crud.sejarah_timeline_delete, name='sejarah_timeline_delete'),
    path('sejarah-timeline/<int:timeline_id>/image/add/', views_crud.sejarah_timeline_image_add, name='sejarah_timeline_image_add'),
    path('sejarah-timeline/image/<int:image_id>/delete/', views_crud.sejarah_timeline_image_delete, name='sejarah_timeline_image_delete'),
    
    path('visi-misi/', views_crud.visi_misi_form, name='visi_misi_form'),
    
    path('program-pendidikan/', views_crud.program_pendidikan_list, name='program_pendidikan_list'),
    path('program-pendidikan/add/', views_crud.program_pendidikan_form, name='program_pendidikan_create'),
    path('program-pendidikan/<int:program_id>/edit/', views_crud.program_pendidikan_form, name='program_pendidikan_update'),
    path('program-pendidikan/<int:program_id>/delete/', views_crud.program_pendidikan_delete, name='program_pendidikan_delete'),
    path('program-pendidikan/<int:program_id>/image/add/', views_crud.program_pendidikan_image_add, name='program_pendidikan_image_add'),
    path('program-pendidikan/image/<int:image_id>/delete/', views_crud.program_pendidikan_image_delete, name='program_pendidikan_image_delete'),
    
    path('fasilitas/', views_crud.fasilitas_list, name='fasilitas_list'),
    path('fasilitas/add/', views_crud.fasilitas_form, name='fasilitas_create'),
    path('fasilitas/<int:fasilitas_id>/edit/', views_crud.fasilitas_form, name='fasilitas_update'),
    path('fasilitas/<int:fasilitas_id>/delete/', views_crud.fasilitas_delete, name='fasilitas_delete'),
    
    path('ekstrakurikuler/', views_crud.ekstrakurikuler_list, name='ekstrakurikuler_list'),
    path('ekstrakurikuler/add/', views_crud.ekstrakurikuler_form, name='ekstrakurikuler_create'),
    path('ekstrakurikuler/<int:ekstra_id>/edit/', views_crud.ekstrakurikuler_form, name='ekstrakurikuler_update'),
    path('ekstrakurikuler/<int:ekstra_id>/delete/', views_crud.ekstrakurikuler_delete, name='ekstrakurikuler_delete'),
    path('ekstrakurikuler/<int:ekstra_id>/image/add/', views_crud.ekstrakurikuler_image_add, name='ekstrakurikuler_image_add'),
    path('ekstrakurikuler/image/<int:image_id>/delete/', views_crud.ekstrakurikuler_image_delete, name='ekstrakurikuler_image_delete'),
    
    path('jadwal-harian/', views_crud.jadwal_harian_list, name='jadwal_harian_list'),
    path('jadwal-harian/add/', views_crud.jadwal_harian_form, name='jadwal_harian_create'),
    path('jadwal-harian/<int:jadwal_id>/edit/', views_crud.jadwal_harian_form, name='jadwal_harian_update'),
    path('jadwal-harian/<int:jadwal_id>/delete/', views_crud.jadwal_harian_delete, name='jadwal_harian_delete'),
    
    path('persyaratan/', views_crud.persyaratan_form, name='persyaratan_form'),
    
    path('alur-pendaftaran/', views_crud.alur_pendaftaran_form, name='alur_pendaftaran_form'),
    
    path('biaya-pendidikan/', views_crud.biaya_pendidikan_list, name='biaya_pendidikan_list'),
    path('biaya-pendidikan/add/', views_crud.biaya_pendidikan_form, name='biaya_pendidikan_create'),
    path('biaya-pendidikan/<int:biaya_id>/edit/', views_crud.biaya_pendidikan_form, name='biaya_pendidikan_update'),
    path('biaya-pendidikan/<int:biaya_id>/delete/', views_crud.biaya_pendidikan_delete, name='biaya_pendidikan_delete'),
    
    path('contact-person/', views_crud.contact_person_list, name='contact_person_list'),
    path('contact-person/add/', views_crud.contact_person_form, name='contact_person_create'),
    path('contact-person/<int:contact_id>/edit/', views_crud.contact_person_form, name='contact_person_update'),
    path('contact-person/<int:contact_id>/delete/', views_crud.contact_person_delete, name='contact_person_delete'),
    
    path('social-media/', views_crud.social_media_list, name='social_media_list'),
    path('social-media/add/', views_crud.social_media_form, name='social_media_create'),
    path('social-media/<int:social_id>/edit/', views_crud.social_media_form, name='social_media_update'),
    path('social-media/<int:social_id>/delete/', views_crud.social_media_delete, name='social_media_delete'),
    
    path('seragam/', views_crud.seragam_list, name='seragam_list'),
    path('seragam/add/', views_crud.seragam_form, name='seragam_create'),
    path('seragam/<int:seragam_id>/edit/', views_crud.seragam_form, name='seragam_update'),
    path('seragam/<int:seragam_id>/delete/', views_crud.seragam_delete, name='seragam_delete'),
    
    path('kmi/', views_crud.kmi_form, name='kmi_form'),
    
    path('statistik/', views_crud.statistik_list, name='statistik_list'),
    path('statistik/add/', views_crud.statistik_form, name='statistik_create'),
    path('statistik/<int:statistik_id>/edit/', views_crud.statistik_form, name='statistik_update'),
    path('statistik/<int:statistik_id>/delete/', views_crud.statistik_delete, name='statistik_delete'),
    
    # Media CRUD (Galeri & Video)
    path('media/', views_crud.media_list, name='media_list'),
    path('media/add/', views_crud.media_form, name='media_create'),
    path('media/<int:media_id>/edit/', views_crud.media_form, name='media_update'),
    path('media/<int:media_id>/delete/', views_crud.media_delete, name='media_delete'),
    
    # Dokumentasi CRUD
    path('dokumentasi/', views_crud.dokumentasi_list, name='dokumentasi_list'),
    path('dokumentasi/add/', views_crud.dokumentasi_form, name='dokumentasi_create'),
    path('dokumentasi/<int:dokumentasi_id>/edit/', views_crud.dokumentasi_form, name='dokumentasi_update'),
    path('dokumentasi/<int:dokumentasi_id>/delete/', views_crud.dokumentasi_delete, name='dokumentasi_delete'),
    path('dokumentasi/<int:dokumentasi_id>/image/add/', views_crud.dokumentasi_image_add, name='dokumentasi_image_add'),
    path('dokumentasi/image/<int:image_id>/delete/', views_crud.dokumentasi_image_delete, name='dokumentasi_image_delete'),
    
    # Informasi Tambahan CRUD
    path('informasi-tambahan/', views_crud.informasi_tambahan_list, name='informasi_tambahan_list'),
    path('informasi-tambahan/add/', views_crud.informasi_tambahan_form, name='informasi_tambahan_create'),
    path('informasi-tambahan/<int:informasi_id>/edit/', views_crud.informasi_tambahan_form, name='informasi_tambahan_update'),
    path('informasi-tambahan/<int:informasi_id>/delete/', views_crud.informasi_tambahan_delete, name='informasi_tambahan_delete'),
    
]
