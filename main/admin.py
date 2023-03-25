from django.contrib import admin
from .models import PageBlock, ThemeSettings, Page, URLPattern, Template, Redirect, Photo, FeedBack


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    pass

@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(URLPattern)
class URLPatternAdmin(admin.ModelAdmin):
    pass


class PageBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'template')

admin.site.register(PageBlock, PageBlockAdmin)


@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass
