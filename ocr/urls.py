from . import views
from django.urls import path


app_name = 'ocr'
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete_content, name='delete'),
    path('generate-pdf/<int:id>/', views.generate_pdf, name='generate-pdf'),
]
