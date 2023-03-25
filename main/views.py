#from django.shortcuts import render
from .models import PageBlock, Page, URLPattern
from .forms import FeedBackForm
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
    model = Page
    template_name = 'index.html'
    context_object_name = 'page'

    def get_object(self):
        return get_object_or_404(Page, slug='index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Здесь добавляйте дополнительный контекст
        context['feedback_form'] = FeedBackForm()
        context['page_blocks'] = self.get_object().blocks.all()
        return context

class AboutUsView(TemplateView):
    """Представление страницы информации о нас"""
    template_name = "about.html"


@csrf_exempt
@require_POST
def feedback(request):
    form = FeedBackForm(request.POST)

    if form.is_valid():
        feedback = form.save()
        return JsonResponse({'status': 'success', 'message': 'Форма успешно отправлена.'}, status=200)
    else:
        return JsonResponse(form.errors, status=400)
    

def url_pattern_page(request, slug):
    url_pattern = get_object_or_404(URLPattern, path=slug)
    context = {}
    context['page']= url_pattern.page
    context['feedback_form'] = FeedBackForm()
    return render(request, 'index.html', context)