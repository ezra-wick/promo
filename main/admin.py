from django.contrib import admin
from .models import PageBlock

class PageBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'template')

admin.site.register(PageBlock, PageBlockAdmin)
