from django import forms
from images.models import Image
from django.utils.text import slugify
from django.core.files.base import ContentFile
from urllib import request

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

        widgets = {
            'url':forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        vaid_extensions = ['jpeg', 'jpg', 'png']
        extension = url.rsplit('.',1)[1].lower()  # obtain the extension of the image
        if extension not in vaid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extension(png, jpg, jpeg)')
        return url

    # we are going to override the save method of the model form
    # to download the bookmarked image from teh provided url everytime
    # the a new form is saved.
    def save(self, force_insert=False,
                    force_update=False,
                    commit=True):
        # get image
        image = super(ImageCreateForm, self).save(commit=False)
        # get url
        image_name = '{}.{}'.format(image.title,
                                        self.cleaned_data['url'].rsplit('.',1)[1].lower())
        downloaded_image = request.urlopen(self.cleaned_data['url'])
        image.image.save(image_name,
                        ContentFile(downloaded_image.read()),
                        save=False)
        if commit:
            image.save()
        return image
 

