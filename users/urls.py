from django.urls import path
from .views import *
from django.contrib.auth import views as authview

app_name="users"
urlpatterns=[
    path("",Users.as_view(),name='user_list'),
    path("register/",RegisterView.as_view(),name='register'),
    path("login/",Login.as_view(),name='login'),
    path("logout/",Logout.as_view(),name='logout'),
    path("myprofile/",Userprov.as_view(),name='myprofile'),
    path("<int:pk>/",UserPosts.as_view(),name='user_posts'),
    path("update-profile/<slug:slug>",UserProfileUpdatev.as_view(),name="update_profile"),
    path("password-change/",authview.PasswordChangeView.as_view(),name='password_change'),
    path("password-done/",authview.PasswordChangeDoneView.as_view(),name='password_change_done'),

]