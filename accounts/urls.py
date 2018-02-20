from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordResetCompleteView .as_view(), name='password_change_done'),
]