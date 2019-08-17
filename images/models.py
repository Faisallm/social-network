from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):

    # user object that bookmarks the image.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            related_name='images_created')  # user.images_created.all()
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, blank=True)
    url = models.URLField()  # will store the original url of the image
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
                                db_index=True)
    # auto_now_add: date is autmatically added when object is created.
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            related_name='images_liked')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])

    # override the save() function of the Image class
    # so as to automatically save the slug based on the title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)