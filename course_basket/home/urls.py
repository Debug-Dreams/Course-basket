from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'landing-page'),
    path('about', views.about, name = 'about-page')
]

