from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    # List santri untuk generate Excel
    path('', views.document_list, name='list'),
    
    # Tutorial Mail Merge
    path('tutorial/', views.tutorial, name='tutorial'),
    
    # Generate Excel untuk Mail Merge
    path('generate/', views.generate_excel, name='generate_excel'),
    path('generate/<int:santri_id>/', views.generate_excel, name='generate_excel_single'),
]

