from accounts.forms import UserRegistrationForm, UserProfileForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        uf = UserRegistrationForm(request.POST, prefix='user')      # user account form
        upf = UserProfileForm(request.POST, prefix='userprofile')   # user profile form
        if uf.is_valid() * upf.is_valid():
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.user = user
            userprofile.save()
            return redirect('home')
    else:
        uf = UserRegistrationForm(prefix='user')
        upf = UserProfileForm(prefix='userprofile')
    return render(request, 'signup.html', {'userform': uf, 'userprofileform': upf})