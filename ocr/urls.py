from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'ocr'
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete_content, name='delete'),
    path('convert-pdf/<int:pk>/', views.convert_to_pdf, name='convert'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
