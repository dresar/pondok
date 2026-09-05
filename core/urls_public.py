"""
Public URLs untuk Website
"""
from django.urls import path
from . import views_public

app_name = 'public'

urlpatterns = [
    path('', views_public.home, name='home'),
    path('blog/', views_public.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views_public.blog_detail, name='blog_detail'),
    path('tenaga-pengajar/', views_public.tenaga_pengajar_list, name='tenaga_pengajar_list'),
    path('tenaga-pengajar/<int:pengajar_id>/json/', views_public.tenaga_pengajar_detail_json, name='tenaga_pengajar_detail_json'),
]

