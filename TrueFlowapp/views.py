from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from TrueFlowapp.models import *
import re


# Create your views here.
def home(request):
    return render(request,'home.html')

def login_user(request):
    if request.method == 'POST':
        print("CSRF Token from POST:", request.POST.get('csrfmiddlewaretoken'))
        print("CSRF Token from Cookie:", request.META.get('CSRF_COOKIE'))
        email = request.POST.get('email','').strip()
        password = request.POST.get('password').strip()
        
        if not email or not password:
            messages.error(request,'Please provide both email and password')
            return render(request,'login.html')
        try:
            user_obj = User.objects.get(email = email)

            user = authenticate(request,username = user_obj.username,password = password)

        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request,user)
            messages.success(request,"You are now logged in!")

            if user.is_superuser:
                return redirect('admin-dashboard')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid Credentials')
            return render(request,'login.html')

    return render(request,'login.html')            

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name','').strip()
        email = request.POST.get('email','').strip()
        phone = request.POST.get('phone').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()

        if not all([name,email,phone,password,confirm_password]):
            messages.error(request,'All fields are Required')
            return render(request,'register.html')
        
        if password != confirm_password:
            messages.error(request,'Passwords do not match')
            return render(request,'register.html')
        
        if len(password) < 8:
            messages.error(request,'Password must be at least 8 characters long')
            return render(request,'register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return render(request,'register.html')
        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
        
        try:
            user = User.objects.create_user(
                username= name,
                email= email,
                password= password
            )
            user.phone = phone
            user.save()

            messages.success(request,'Account Created Successfully! You can now login!')
            return redirect('login')
        except Exception as e:
            messages.error(request,f'Error creating account:{str(e)}')
            return render(request,'register.html')
    return render(request,'register.html')    


def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out successfully!')
    return redirect('home')



def dashboard(request):
    return render(request,'dashboard.html')

def buyWater(request):
    return render(request,'buy-water.html')
def admin(request):
    return render(request,'admin.html')
