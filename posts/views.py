from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm 
from django.urls import reverse_lazy, reverse


# Create your views here.
def index(request):
    #If the method is POST
    if request.method=='POST':
        form= PostForm(request.POST, request.FILES)
        #If the form is valid
        if form.is_valid():
            #If yes, save
            form.save()
            #Redirect to home
            return HttpResponseRedirect('/')

        else:
            #If no, show error
            return HttpResponseRedirect(form.erros.as_json())

    #Get all posts, limit= 20
    posts = Post.objects.all().order_by('-created_at')[:20]     
    #Show
    return render(request, 'posts.html',
                    {'posts' : posts})
                
def delete(request, post_id):
    #Find post
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')
    

def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    # Find post
    # if request.method == “GET”:
    # post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        # editpost = Post.objects.get(id=post_id)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect(form.errors.as_json())
    form = PostForm
    # form = PostForm
    # show
    return render(request, 'edit.html', {'post': post, 'form': form})

def like(request, post_id):
    like = Post.objects.get(id=post_id)
    like.likes +=1
    like.save()
    return HttpResponseRedirect('/')
