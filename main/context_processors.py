from .models import Page, ThemeSettings

def theme_settings(request):
    try:
        page = Page.objects.get(slug=request.path.strip('/'))
        settings = page.theme
    except Page.DoesNotExist:
        settings = ThemeSettings.objects.first()

    return {'theme_settings': settings}