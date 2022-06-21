from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import *
from .models import *


ObjectDoesNotExist=404
# Create your views here.
def index(request): 
    return render(request, 'home.html')

def register(request):
    if request.method== "POST":
        username=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]
        if password1 != password2:
            messages.error(request,"Your Passwords do not Match!! Please Try Again")
            return redirect('/register')
        new_user=User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )
        new_user.save()
        return render (request,'userlogin.html')
    return render(request,'register.html')

def signin(request):
    if request.method== "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have successfuly logged in")
            return redirect ('hoods') 
    return render(request, 'userlogin.html')


def signout(request):
    logout(request)
    messages.success(request,"You have logged out successfuly")
    return redirect ('home')


def new_hood(request):
    if request.method == 'POST':
        form = HoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user.profile
            hood.save()
            return redirect('hoods')
    else:
        form = HoodForm()
    return render(request, 'new-hood.html', {'form': form})


@login_required(login_url='userlogin')
def hoods(request):
    hoods = Hood.objects.all()
    if request.method == 'POST':
        form = HoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user.profile
            hood.save()
            return redirect('hoods')
    else:
        form = HoodForm()
    hoods: hoods
    return render(request, 'hoods.html',{"hoods":hoods,"form": form})

def join_hood(request, hood_id):
    try:
        hood = Hood.objects.get(id=hood_id)
    except ObjectDoesNotExist:
        return Http404
    request.user.profile.location = hood
    hood.save()
    return redirect('one-hood',id)

def one_hood(request, hood_id):
    hood = Hood.objects.get(id=hood_id)
    jobs = Business.objects.filter(neighbourhood=hood)
    residents = Profile.objects.filter(location = hood)
    posts = Post.objects.filter(hood=hood)
    jobs= jobs[::-1]
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.neighbourhood = hood
            b_form.user = request.user.profile
            b_form.save()
            return redirect('one-hood', hood.id)
    else:
        form = BusinessForm()
    params = {
        'hood': hood,
        'business': jobs,
        'form': form,
        'posts': posts,
        'residents':residents
    }
    return render(request, 'one-hood.html', params)

def add_business(request, hood_id):
    if request.method == 'POST':
        hood = Hood.objects.get(id =hood_id)
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            bs_form = form.save(commit=False)
            bs_form.hood = hood
            bs_form.owner = request.user.profile
            bs_form.create_business()
            return redirect('one-hood', hood.id)
    else:
        form = BusinessForm()

    return render(request, 'business.html', {"form" : form})

def new_post(request, hood_id):
    hood = Hood.objects.get(id =hood_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.hood = hood
            news.user = request.user.profile
            news.save()
            return redirect('one-hood', hood.id)
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})

@login_required(login_url='userlogin')
def myprofile(request):
    user = request.user
    user:user
    return render(request, 'myprofile.html', {'user':user})

def edit_profile(request, username):
    user = User.objects.get(username = username)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance = request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('myprofile')
    else: 
        form = EditProfileForm(instance = request.user.profile)
    return render(request, 'updateprofile.html', {'form': form})

def leave_hood(request, id):
    try:
        hood = Hood.objects.get(id =id)
    except ObjectDoesNotExist:
        return Http404
    request.user.profile.location = None
    request.user.profile.save()
    return redirect('hoods')

def search_business(request):
    if request.method == 'GET':
        name = request.GET.get("title")
        results = Business.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        ctx = {
            'results': results,
            'message': message
        }
        return render(request, 'searchresults.html', ctx)
    else:
        message = "You haven't searched for any business"
    return render(request, "one-hood.html")


