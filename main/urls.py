from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('feedback/', views.feedback, name='feedback'),
]

urlpatterns.append(re_path(r'^(?P<slug>[-\w]+)/$', views.url_pattern_page, name='url_pattern_page'))