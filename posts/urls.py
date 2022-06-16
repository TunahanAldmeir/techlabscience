from django.urls import path

from users.views import Login, Logout, RegisterView
from .views import *

urlpatterns=[
    path("",index_wiev.as_view(),name="index"),
    path('detail/<int:pk>/<slug:slug>',PostDetailView.as_view(),name="detail"),
    path('post-update/<int:pk>/<slug:slug>',UpdatePostView.as_view(),name="post_update"),
    path('category/<int:pk>',CategoryDetail.as_view(),name='category_detail'),
    path('tag/<slug:slug>',TagDetail.as_view(),name='tag_detail'),
    path("login/",Login.as_view(),name='login'),
    path("logout/",Logout.as_view(),name='logout'),
    path("post-create/",PostCreateView.as_view(),name='create_post'),
    path("register/",RegisterView.as_view(),name='register'),
    path("post-delete/<int:pk>/<slug:slug>",DeletePostView.as_view(),name='delete_post'),
    path('search/',SearhView.as_view(),name='search'),


]

