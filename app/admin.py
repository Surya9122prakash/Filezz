from django.contrib import admin
from .models import UploadedFile,ContactMessage

# Register your models here.
admin.site.register(UploadedFile)
admin.site.register(ContactMessage)