from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from account.models import Profile
from django.contrib import messages



def user_login(request):
    
    if request.method == "POST":
        form = LoginForm(data=request.POST)  # prepopulate form with data.

        if form.is_valid():
            cd = form.cleaned_data

            # authenticate users against the database
            user = authenticate(request, username=cd['username'], password=cd['password'])
            # returns user or None

            if user is not None:
                if user.is_active:
                    # login user into the current session
                    login(request, user)
                    return HttpResponse("User has logged in. Authenticated Successfully")

                else:
                    return HttpResponse("Your account is no more active. it has being blocked.")

            else:
                return HttpResponse("Username or Password is not correct.")    

    else:
        form = LoginForm()

    return render(request,
                    'account/login.html',
                    {'form':form})
        
@login_required
def dashboard(request):
    return render(request,
                 'account/dashboard.html',
                 {'section':'dashboard'})

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            cd = form.cleaned_data  # obtain user's data
            # create new user's instance but don't save to the database yet.
            new_user = form.save(commit=False)
            new_user.set_password(cd['password'])
            # create a new profile for a new user
            Profile.objects.create(user=new_user)
            new_user.save()
            return render(request,
                            'account/register_done.html',
                            {'new_user':new_user})
    else:
        form = UserRegistrationForm()  # empty form of user.

    return render(request,
                    'account/register.html',
                    {'form':form})

@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(data=request.POST,
                                    instance=request.user)
        profile_form = ProfileEditForm(data=request.POST,
                                    instance=request.user.profile,
                                    files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile Updated successfully.')

        else:
            messages.error(request, "Error updating your profile.")

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                'account/edit.html',
                {'profile_form':profile_form,
                'user_form':user_form})