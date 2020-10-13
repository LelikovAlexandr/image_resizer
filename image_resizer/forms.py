from django import forms
from django.core.exceptions import ValidationError

ALLOW_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']


class UploadImageForm(forms.Form):
    url = forms.URLField(label='Ссылка', required=False)
    image = forms.ImageField(label='Файл', required=False)

    def clean(self):
        data = self.cleaned_data
        if bool(data.get('image')) == bool(data.get('url')):
            raise forms.ValidationError('Please fill one field')

        if not data.get('url').split('.')[-1] in ALLOW_EXTENSIONS and not data.get('image'):
            raise ValidationError('Invalid extension', code='invalid')

        return data


class ResizeImageForm(forms.Form):
    width = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)

    def clean_width(self):
        width = self.cleaned_data.get('width') or 0
        if width < 0:
            raise ValidationError('Input positive number')
        return width

    def clean_height(self):
        height = self.cleaned_data.get('height') or 0
        if height < 0:
            raise ValidationError('Input positive number')
        return height
