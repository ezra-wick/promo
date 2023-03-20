from django.urls import path
from .views import *

urlpatterns = [
    # path('', views.index, name='index'),
    # path('about/', views.about, name='about'),
    path('', IndexPage.as_view(), name='index'),
    path('about/', AboutUsView.as_view(), name='about'),
]
