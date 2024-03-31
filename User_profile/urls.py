from django.urls import path
from .views import Profile ,Home ,Signup , Update,Profile_page ,Login ,Log_out,search
from django.contrib.auth import views as auth_views



urlpatterns = [
    
    # my ursl 
    path('',Home,name='home'),
    path('sign_up/', Signup ,name = 'signup'),
    path('log_in/', Login ,name = 'login'),
    path('log_out/', Log_out ,name = 'logout'),
    path('update/<int:pk>/',Update,name='update'),
    path('search/',search,name='search'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
        name='password_reset_complete'),

    
    path('<int:pk>/profile/', Profile_page , name = 'profile'),

]
