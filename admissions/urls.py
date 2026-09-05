from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('success/', views.success_view, name='success'),
]

