from .forms import UserRegistrationForm, UserProfileForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        uf = UserRegistrationForm(request.POST, prefix='user')      # user account form
        upf = UserProfileForm(request.POST, prefix='userprofile')   # user profile form
        if uf.is_valid() * upf.is_valid():
            user = uf.save()
            # sign the user in to their new account
            user = authenticate(username=uf.cleaned_data['username'],
                                password=uf.cleaned_data['password1'],)
            if user is not None:
                login(request, user)
                userprofile = upf.save(commit=False)
                userprofile.user = user
                userprofile.save()
                return render(request, 'signup_success.html')
    else:
        uf = UserRegistrationForm(prefix='user')
        upf = UserProfileForm(prefix='userprofile')
    return render(request, 'signup.html', {'userform': uf, 'userprofileform': upf})

def signin(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            cd = loginForm.cleaned_data
            user = authenticate(username=cd['username'], 
                                password=cd['password'])
            if user is not None:
                login(request, user)
                return render(request, 'signup_success.html')
            else:
                return render(request, 'signin.html', {'loginForm': loginForm})
    else:
        loginForm = LoginForm(request.POST)
    return render(request, 'signin.html', {'loginForm': loginForm})

def signout(request):
    logout(request)
    return render(request, 'signout_success.html')