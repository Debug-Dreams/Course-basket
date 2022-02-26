from django.shortcuts import render
from django.http import HttpResponse
from .models import Course

# Create your views here.

courses = [
    {
        'id': 'IC111',
        'name': 'Linear Algebra',
        'semester': '1',
        'ltpc': '1-2-3-4',
        'branch': 'ALL'
    },
    {
        'id': 'IC152',
        'name': 'DS1',
        'semester': '1',
        'ltpc': '1-2-3-4',
        'branch': 'ALL'
    },
    {
        'id': 'IC252',
        'name': 'DS3',
        'semester': '1',
        'ltpc': '1-2-3-4',
        'branch': 'ALL'
    }
]

def home(request):

    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'home/index.html',context)

def about(request):
    return render(request, 'home/about.html' )