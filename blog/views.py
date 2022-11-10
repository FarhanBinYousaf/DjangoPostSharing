from django.shortcuts import render,get_object_or_404
#  This login required will work along with class based views, b/c decorator not works with class based views
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ( 
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
# Create your views here.

def index(request):
    post = Post.objects.all()
    context = {'posts':post}
    return render(request,'blog/index.html',context)

# Below is the class based list view => which shows the list of objects in specified model 
class PostListView(ListView):
    # name of model
    model = Post
    # template of that page where posts will be showen
    template_name = 'blog/index.html'   #Name of template should be in this formate: <app_name>/<model_name>_<view_type>.html
    # this is the context dictionary from index() fun.
    context_object_name = 'posts'
    # This is the ordering of post according to latest post => latest post will be on top
    ordering = ['-date_posted']

    paginate_by = 5


# This class based view is codded for the purpose when any user clicks on "author link of post page" then that user will be shown the total posts posted by that corredposing user 
# In this username will be passed in "url"
class UserPostListView(ListView):
    # name of model
    model = Post
    # template of that page where posts will be showen
    template_name = 'blog/user_posts.html'   #Name of template should be in this formate: <app_name>/<model_name>_<view_type>.html
    # this is the context dictionary from index() fun.
    context_object_name = 'posts'
    # This is the ordering of post according to latest post => latest post will be on top
    # ordering = ['-date_posted']
    paginate_by = 5

    # This below fun. is for , this will give the username that is passed in url 
    # For this purpose first import the get_subject_or_404 top of the page
    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

# Below is the class based detail view => which shows the detail of individual post in specified model
# It takes the default page for individual post which is post_detail.html and now i have created that page 
# In PostDetailView() => a unique id called pk(primary key) is called against every post and that id is passed in url

class PostDetailView(DetailView):
    # name of model
    model = Post

#  This class based view is PostCreateView is for creating new post
# LoginRequiredMixin => is for login required b/c login decorator is not used with class based views
class PostCreateView(LoginRequiredMixin, CreateView):
    # name of model
    model = Post
    fields = ['title','content']

    # This code form_valid() is for validating form which means only author can post. 
    # Every post should have an author and here author would be logged in user, that's 
    # why request.user is used

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# LoginRequiredMixin => is for login required b/c login decorator is not used with class based views
# UserPassesTestMixin => it only update the logged in user's post to update
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # name of model
    model = Post
    fields = ['title','content']

    # This code form_valid() is for validating form which means only author can post. 
    # Every post should have an author and here author would be logged in user, that's 
    # why request.user is used

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # This function is coded for when we access another user's post to update then it will return false, 
    # logged in user can update or delete it's post, logged in user cannot update or delete post of another user's post
    # Before we code this , first import "UserPassesTestMixin" on the top of page
    def test_func(self):
        post = self.get_object()    # gets the currently post
        if self.request.user == post.author:   # if logged in user equals to that post's author 
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    # name of model
    model = Post
    # success_url => will redirect the user after deleting post to home page this => '/' means to home page
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()    # gets the currently post
        if self.request.user == post.author:   # if logged in user equals to that post's author 
            return True
        return False

def about(request):
    return render(request,'blog/about.html')
