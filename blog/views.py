from asyncio.windows_events import NULL
from ctypes import sizeof
from queue import Empty
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Blogpost

# Create your views here.


def index(request):
    myposts = Blogpost.objects.all()
    return render(request, 'blog/index.html', {'myposts': myposts})


def blogpost(request, id):
    post = Blogpost.objects.filter(post_id=id)[0]
    prev = NULL
    next = NULL
    if(bool(Blogpost.objects.filter(post_id=id-1))):
        prev = Blogpost.objects.filter(post_id=id-1)[0]

    if(bool(Blogpost.objects.filter(post_id=id+1))):
        next = Blogpost.objects.filter(post_id=id+1)[0]
    # print(post)
    return render(request, 'blog/blogpost.html', {'post': post, 'prev': prev, 'next': next})
