"""
URL Configuration untuk Blog Management
"""
from django.urls import path
from . import views, views_crud

app_name = 'blog'

urlpatterns = [
    # Blog Post URLs
    path('', views.blog_list, name='list'),
    path('add/', views.blog_create, name='create'),
    path('<int:blog_id>/', views.blog_detail, name='detail'),
    path('<int:blog_id>/edit/', views.blog_update, name='update'),
    path('<int:blog_id>/delete/', views.blog_delete, name='delete'),
    
    # Statistics URLs
    path('<int:blog_id>/like/', views.blog_increment_likes, name='increment_likes'),
    path('<int:blog_id>/share/', views.blog_increment_shares, name='increment_shares'),
    
    # Category CRUD
    path('category/', views_crud.category_list, name='category_list'),
    path('category/add/', views_crud.category_form, name='category_create'),
    path('category/<int:category_id>/edit/', views_crud.category_form, name='category_update'),
    path('category/<int:category_id>/delete/', views_crud.category_delete, name='category_delete'),
    
    # Tag CRUD
    path('tag/', views_crud.tag_list, name='tag_list'),
    path('tag/add/', views_crud.tag_form, name='tag_create'),
    path('tag/<int:tag_id>/edit/', views_crud.tag_form, name='tag_update'),
    path('tag/<int:tag_id>/delete/', views_crud.tag_delete, name='tag_delete'),
    
    # Testimoni CRUD
    path('testimoni/', views_crud.testimoni_list, name='testimoni_list'),
    path('testimoni/add/', views_crud.testimoni_form, name='testimoni_create'),
    path('testimoni/<int:testimoni_id>/edit/', views_crud.testimoni_form, name='testimoni_update'),
    path('testimoni/<int:testimoni_id>/delete/', views_crud.testimoni_delete, name='testimoni_delete'),
    
    # Pengumuman CRUD
    path('pengumuman/', views_crud.pengumuman_list, name='pengumuman_list'),
    path('pengumuman/add/', views_crud.pengumuman_form, name='pengumuman_create'),
    path('pengumuman/<int:pengumuman_id>/edit/', views_crud.pengumuman_form, name='pengumuman_update'),
    path('pengumuman/<int:pengumuman_id>/delete/', views_crud.pengumuman_delete, name='pengumuman_delete'),
]

