from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('about/',about,name='about'),
    path('store/',store,name='store'),
    path('review/',review,name='review'),
    path('contact/',contact,name='contact'),
    path('subscribe/',subscribe,name='subscribe'),
    path('broadcast/', broadcast_email, name='broadcast_email'),
    # accounts
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
]
