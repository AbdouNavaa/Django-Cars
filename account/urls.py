
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

app_name='account'

urlpatterns = [
    path('signup',views.signup , name='signup'),
    path('',views.login , name='login'),
    path('logout/',views.logout , name='logout'),
    path('profile<str:user>',views.profile , name='profile'),
    path('profile/edit',views.profile_edit , name='profile_edit'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    

]