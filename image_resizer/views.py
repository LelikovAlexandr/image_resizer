from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from requests import RequestException

from image_resizer.forms import UploadImageForm, ResizeImageForm
from image_resizer.models import Image


class ImagesList(ListView):
    model = Image
    template_name = 'images_list.html'


def upload_image(request):
    if request.method == 'GET':
        form = UploadImageForm()
        return render(request, 'upload_image.html', {'form': form})

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            url = request.POST.get('url')
            if url:
                image = Image()
                try:
                    image.download_image(url)
                except RequestException:
                    return render(request, 'upload_image.html', {
                        'errors': 'Изображение по ссылке не найдено',
                        'form': form
                    })
            else:
                image = Image(image=request.FILES.get('image'))
            image.save()
            return HttpResponseRedirect(image.get_absolute_url())

        return render(request, 'upload_image.html', {'form': form})


def resize_image(request, pk):
    form = ResizeImageForm(request.POST)
    width = request.POST.get('width') or 0
    height = request.POST.get('height') or 0
    image = Image.objects.get(pk=pk)
    if width or height:
        if form.is_valid():
            resized_img_url = image.get_resize_image_url(int(width), int(height))
            return render(request, 'resize_image.html',
                          {'resized_img_url': resized_img_url, 'image': image, 'form': form})
    return render(request, 'resize_image.html', {'image': image, 'form': form})
