from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from image_resizer import views

urlpatterns = [
    path('', views.ImagesList.as_view(), name='image_list'),
    path('upload/', views.UploadImage.as_view(), name='upload'),
    path('<int:pk>/', views.ResizeImage.as_view(), name='resize_image'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
