from django.urls import path
from . import views

app_name = 'file_converter'

urlpatterns = [
    path('', views.convert_file, name='convert_file'),
    path('success/<int:pk>/', views.conversion_success, name='conversion_success'),
    path('upload/', views.upload_document, name='upload_document'),
    path('edit/<int:pk>/', views.edit_document, name='edit_document'),
]