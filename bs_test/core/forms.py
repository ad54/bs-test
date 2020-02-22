from django.forms import ModelForm
from core.models import Image

class ImageUploadForm(ModelForm):
    class Meta:
        model = Image
        fields = ['img','tags']

class ImageSearchForm(ModelForm):
    class Meta:
        model = Image
        fields = ['tags']