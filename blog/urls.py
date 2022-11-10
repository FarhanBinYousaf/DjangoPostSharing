from django.urls import path
from . import views
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
    )

urlpatterns = [
    path('',PostListView.as_view(),name="index"),
    path('user/<str:username>/',UserPostListView.as_view(),name="user-posts"),
    # pk(primary key) is passed in url. 
    path('post/<int:pk>/',PostDetailView.as_view(),name="post-detail"),
    # This is for creating new post
    path('post/new/',PostCreateView.as_view(),name="post-form"),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name="post-update"),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name="post-delete"),
    path('about',views.about,name="about"),
]