from django.contrib import admin
from .models import VideoUpload

# Register your models here.
admin.site.register(VideoUpload)
admin.site.site_header = 'MOMENT LOCALIZER'
admin.site.site_title = 'MOMENT LOCALIZER PORTAL'
admin.site.index_title = 'Welcome to the MOMENT LOCALIZER ADMIN!'
