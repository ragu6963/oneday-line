from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Profile
from django.core.paginator import Paginator
from django.contrib.auth.models import User
import datetime  
def home(request):
    try:   
        user = User.objects.get(username=request.user.get_username()) 
        dt = datetime.datetime.now()
        
        user_date = user.profile.last_date.strftime("%Y-%m-%d") 
        now_date = dt.strftime("%Y-%m-%d") 
        time_check = False

        if now_date == user_date:
            time_check = True  

        blog_list = Blog.objects.all().order_by('-id')
        paginator = Paginator(blog_list, 3)  # 블로그 객체 %d개를 한페이지로 자르기
        page = request.GET.get('page')  # request된 페이지를 알아내고
        posts = paginator.get_page(page)  # request된 페이지를 얻어낸다

        if request.user.is_authenticated == True:
            condition = "인증"
        else:
            condition = "비인증"

        return render(request, 'home.html', {'posts': posts, 'condition': condition,'user':user,'time_check':time_check,'user_date':user_date})

    except :
        blog_list = Blog.objects.all().order_by('-id')
        paginator = Paginator(blog_list, 3)  # 블로그 객체 %d개를 한페이지로 자르기
        page = request.GET.get('page')  # request된 페이지를 알아내고
        posts = paginator.get_page(page)  # request된 페이지를 얻어낸다

        if request.user.is_authenticated == True:
            condition = "인증"
        else:
            condition = "비인증"

        return render(request, 'home.html', {'posts': posts, 'condition': condition})

def new(request):
    if request.method == "POST":
        blog = Blog()
        blog.body = request.POST['body']
        user_id = request.POST['user_id']
        user = User.objects.get(pk=user_id)
        user.profile.last_date = datetime.datetime.now()
        blog.user = user 
        blog.save()
        user.save()
        return redirect('home')
    else:
        return redirect('home')

  
 
