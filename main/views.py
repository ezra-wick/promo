from django.shortcuts import render
from .models import PageBlock


def index(request):
    context = {}
    context['page_blocks'] = PageBlock.objects.all()
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')