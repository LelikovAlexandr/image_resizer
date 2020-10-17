from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from requests import RequestException

from image_resizer.forms import UploadImageForm, ResizeImageForm
from image_resizer.models import Image


class ImagesList(ListView):
    model = Image
    template_name = 'images_list.html'


class UploadImage(CreateView):
    model = Image
    template_name = 'upload_image.html'
    form_class = UploadImageForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            url = form.cleaned_data.get('url')
            if not url:
                return super().post(request, *args, **kwargs)
            image = Image()
            try:
                image.download_image(url)
            except RequestException:
                form.add_error(None, "Image by URL doesn't exist")
                return render(request, self.template_name, {'form': form})
            image.save()
            return HttpResponseRedirect(image.get_absolute_url())
        else:
            return render(request, self.template_name, {'form': form})


class ResizeImage(FormMixin, DetailView):
    model = Image
    template_name = 'resize_image.html'
    form_class = ResizeImageForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        image = self.get_object()
        width = request.POST.get('width') or 0
        height = request.POST.get('height') or 0
        if form.is_valid() and (width or height):
            resized_img_url = image.get_resized_image_url(int(width), int(height))
            return render(request, 'resize_image.html',
                          {'resized_img_url': resized_img_url, 'image': image, 'form': form})
        return render(request, self.template_name, {'form': form, 'image': image})
