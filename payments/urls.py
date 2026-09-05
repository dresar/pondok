from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create/<int:santri_id>/', views.create_payment_view, name='create'),
    path('detail/<int:payment_id>/', views.payment_detail_view, name='detail'),
]

