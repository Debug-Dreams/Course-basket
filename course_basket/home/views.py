from django.shortcuts import render
from django.http import HttpResponse
from .models import Course

# Create your views here.

def home(request):

    
    return render(request, 'home/index.html')

def about(request):

    context = {
        'courses': Course.objects.all()
    }

    return render(request, 'home/about.html', context )