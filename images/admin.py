from django.contrib import admin
from images.models import Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'image', 'created')
    list_filter = ('created',)
    raw_id_fields = ('user',)
    date_hierarchy = 'created'
    search_fields = ('user', 'title')

admin.site.register(Image, ImageAdmin)
