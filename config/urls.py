from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from image_resizer import views

urlpatterns = [
    path('', views.ImagesList.as_view(), name='image_list'),
    path('upload/', views.upload_image, name='upload'),
    path('<int:pk>/', views.resize_image, name='image_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
