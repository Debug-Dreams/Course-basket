from pickletools import read_uint1
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functions import *

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

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm( request.POST, request.FILES ,instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated for {request.user.username}')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


    # return render(request, 'users/dashboard.html')

@login_required
def discussion(request):
    return render(request, 'users/discussion-forum.html')

@login_required
def dashboard(request):

    user_courses_completed = request.user.profile.completed_courses.all()
    user_courses_current = request.user.profile.current_courses.all()
    user_courses_sem = get_user_course(request.user)
    user_credits = request.user.profile.total_credits
    basket_comp_msg = check_basket(request)
    
    
    if request.method == 'POST':

        if  'Add' in request.POST:
            to_add = request.POST.get("Add")
            # print("adding")
            
            do_task(request,to_add, "Submit")
            do_task(request, to_add, "update_tot_credits")
            user_courses_sem = update_visible_courses(request)
            basket_comp_msg = check_basket(request)
            # print(user_courses_current)
            messages.success(request, f'Course added successfully')

        if  'drop' in request.POST:
            to_drop = request.POST.get("drop")
            do_task(request,to_drop, "drop")
            do_task(request, to_drop, "update_tot_credits")
            user_courses_sem = update_visible_courses(request)
            basket_comp_msg = check_basket(request)
        
        if  'course_by_sem' in request.POST:
            sem = request.POST.get("course_by_sem","")
            # courses_for_sem = get_user_course(user)
            courses_for_sem = get_course_sem(sem)
        else:
            courses_for_sem = []

    else:
        courses_for_sem = []

    request.user.profile.save()
    print(basket_comp_msg)
    # print(user_courses_completed)
    # print(user_courses_current)
    context = {
        'completed_courses' : user_courses_completed,
        'user_sem' : user_courses_sem,
        'course_filter_sem' : courses_for_sem,
        # 'added_courses' : user_courses_added,
        'current_courses' : user_courses_current,
        'basket_message':basket_comp_msg,
        'total_credits' : user_credits
    }
    return render(request, 'users/dashboard.html', context)



    # show courses and credits left of a person
