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

    current_user = request.user

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm( request.POST, request.FILES ,instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            prev_sem = current_user.profile.sem #add courses to completed courses
            prev_courses = current_user.profile.current_courses.all()
            u_form.save()
            p_form.save()

            new_sem = current_user.profile.sem

            update_comp_courses(request,prev_courses)
            update_curr_courses(request,new_sem)


            current_user.profile.current_courses.all().delete()
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
def todo(request):
    return render(request, 'users/todo.html')

@login_required
def dashboard(request):

    user_courses_completed = request.user.profile.completed_courses.all()
    user_courses_current = request.user.profile.current_courses.all()
    user_courses_sem = get_user_course(request.user)
    user_credits = request.user.profile.total_credits

    basket_comp_msg = check_basket(request)

    curr_sem_credits = 0
    for i in request.user.profile.current_courses.all():
        curr_sem_credits = curr_sem_credits + i.credits
    
    

    if request.method == 'POST':

        if  'Add' in request.POST:
            to_add = request.POST.get("Add")
            # print("adding")   
            do_task(request,to_add, "Submit")

            # for i in request.user.profile.current_courses.all():
            #     curr_sem_credits = curr_sem_credits + i.credits

            # if curr_sem_credits > 24 :
            #     do_task(request,to_add, "drop")
            #     messages.error(request, f'Course not added, Credit Limit reached')
            # else:
            do_task(request, to_add, "update_tot_credits")
            messages.success(request, f'Course added successfully')
            user_courses_sem = update_visible_courses(request)
            basket_comp_msg = check_basket(request)

            
            # print(user_courses_current)

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

# chosen_sem = ["NONE","NONE"]

@login_required
def finished_courses(request):
    current_user = request.user
    current_sem = current_user.profile.sem
    courses_for_sem = []
    select_sem_courses = []
    # global chosen_sem.pop() 
    chosen_sem = "NONE"
    

    if current_sem == "1st":
        return redirect('dashboard')

    if request.method == 'POST':
        if  'Add' in request.POST:
            to_add = request.POST.get("Add")
            # print("adding")   
            do_task_all(request,to_add, "Submit")
            do_task_all(request, to_add, "update_tot_credits")
            messages.success(request, f'Course added successfully')
            # chosen_sem = request.POST.get("course_by_sem","")
            # user_courses_sem = update_visible_courses(request)
            # basket_comp_msg = check_basket(request)

        if  'drop' in request.POST:
            to_drop = request.POST.get("drop")
            do_task_all(request,to_drop, "drop")
            do_task_all(request, to_drop, "update_tot_credits")
            # user_courses_sem = update_visible_courses(request)
            # # chosen_sem = request.POST.get("course_by_sem","")
            # basket_comp_msg = check_basket(request)

        if  'course_by_sem' in request.POST:
            # chosen_sem.append(request.POST.get("course_by_sem",""))
            chosen_sem = request.POST.get("course_by_sem","")
            # courses_for_sem = get_user_course(user)
            # courses_for_sem = get_course_sem(chosen_sem)
            select_sem_courses = get_select_sem_course(request,chosen_sem)
            courses_for_sem = update_visible_courses_prev(request,chosen_sem)
        else:
            courses_for_sem = []
            select_sem_courses = []

    # print(select_sem_courses)
    context = {
        'current_sem' : current_sem,
        'course_filter_sem' : courses_for_sem,
        'selected_sem_courses': select_sem_courses,
        'sem_chosen' : chosen_sem
    }
    return render(request, 'users/finishedCourses.html', context)

    # show courses and credits left of a person

@login_required
def track(request):
    current_user = request.user
    all_courses = current_user.profile.completed_courses.all()
    current_courses = current_user.profile.current_courses.all()
    print(all_courses)

    send_courses = track_page(request)

    ic = all_courses.filter(type = "IC Compulsory").count()
    sci_b1 = all_courses.filter(type = "Science Basket 1").count()
    sci_b2 = all_courses.filter(type = "Science Basket 2").count()
    sci_b3 = all_courses.filter(type = "Science Basket 3").count()
    hss = all_courses.filter(type = "HSS").count()
    dc = all_courses.filter(type = "DE").count()
    fe = all_courses.filter(type = "FE").count()
    mtp = all_courses.filter(type = "").count()

    ic_curr = current_courses.filter(type = "IC Compulsory").count()
    sci_b1_curr = current_courses.filter(type = "Science Basket 1").count()
    sci_b2_curr = current_courses.filter(type = "Science Basket 2").count()
    sci_b3_curr = current_courses.filter(type = "Science Basket 3").count()
    hss_curr = current_courses.filter(type = "HSS").count()
    dc_curr = current_courses.filter(type = "DE").count()
    fe_curr = current_courses.filter(type = "FE").count()
    mtp_curr = current_courses.filter(type = "").count()

    print(ic)

    # |length

    context = {
        'all_courses' : send_courses,
        'ic': ic + ic_curr,
        'ic_left':64-(ic + ic_curr),
        'sci_b1':sci_b1 + sci_b1_curr,
        'sci_b1_left': 3 - sci_b1 - sci_b1_curr,
        'sci_b2' : sci_b2 + sci_b2_curr,
        'sci_b2_left' : 3 - sci_b2 - sci_b2_curr,
        'sci_b3': sci_b3 + sci_b3_curr,
        'sci_b3_left' : 3 - sci_b3 - sci_b3_curr,
        'hss' : hss + hss_curr,
        'hss_left' :18- hss - hss_curr,
        'dc' : dc + dc_curr,
        'dc_left' :33- dc - dc_curr,
        'fe': fe + fe_curr,
        'fe_left':22- fe - fe_curr,
        'mtp': mtp + mtp_curr,
        'mtp_left': 12-mtp - mtp_curr,   
    }

    return render(request, 'users/track.html', context)