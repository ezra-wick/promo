#from django.shortcuts import render
from .models import PageBlock
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _

# def index(request):
#     context = {}
#     context['page_blocks'] = PageBlock.objects.all()
#     return render(request, 'index.html', context)
#
#
# def about(request):
#     return render(request, 'about.html')

class IndexPage(ListView):
    """Представление главной страницы"""
    model = PageBlock
    template_name = 'index.html'
    context_object_name = 'page_blocks'
    #queryset = PageBlock.objects.all()

class AboutUsView(TemplateView):
    """Представление страницы информации о нас"""
    template_name = "about.html"