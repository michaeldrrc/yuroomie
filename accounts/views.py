from .forms import UserRegistrationForm, LoginForm
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from home.models import Room

def signup(request):
    if request.method == 'POST':
        uf = UserRegistrationForm(request.POST)
        if uf.is_valid():
            user = uf.save()
            # sign the user in to their new account
            user = authenticate(username=uf.cleaned_data['username'],
                                password=uf.cleaned_data['password1'],)
            if user is not None:
                login(request, user)
                userprofile = Profile(user=user, year=1)
                userprofile.save()
                return redirect('edit_profile')
    else:
        uf = UserRegistrationForm()
    return render(request, 'signup.html', {'userform': uf})

def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
        profile.major = request.POST['major']
        profile.year = request.POST['year']
        profile.gender = request.POST['gender']
        profile.save()
        return render(request, 'signup_success.html')
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'edit_profile.html', {'profile': profile})


def signin(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            cd = loginForm.cleaned_data
            user = authenticate(username=cd['username'], 
                                password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'signin.html', {'loginForm': loginForm,
                                                        'error_message': 'Your username and password did not match our records'})
    else:
        loginForm = LoginForm(request.POST)
    return render(request, 'signin.html', {'loginForm': loginForm})

def signout(request):
    logout(request)
    return redirect('index')

def user_listings(request):
    user_listings = []
    all_rooms = Room.objects.all()
    for room in all_rooms:
        if request.user.pk == room.creator_id:
            user_listings.append(room)
    return render(request, 'accounts/your_listings.html', {'user_listings': user_listings})