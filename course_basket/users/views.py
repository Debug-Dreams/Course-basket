from pickletools import read_uint1
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}, You can now Login')
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render (request, 'users/register.html', {'form':form } )

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')

@login_required
def discussion(request):
    return render(request, 'users/discussion-forum.html')
