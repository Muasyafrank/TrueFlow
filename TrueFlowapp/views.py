from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import *
from .serializers import UserRegistrationSerializer,LoginSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
import re

User = get_user_model()
def home(request):
    return render(request,'home.html')

def login_user(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data = request.POST)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request,user)
            messages.success(request,'Logged in Successfully!')

            if user.is_superuser:
                return redirect('admin-dashboard')
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'serializer': serializer,
                'errors': serializer.errors,
                'form_data': request.POST  # To repopulate form
            }, status=status.HTTP_400_BAD_REQUEST)
    return render(request,'login.html')
            

     

@api_view(['POST','GET'])          
def register(request):
    if request.method == 'GET':
        serializer = UserRegistrationSerializer()
        return render(request,'register.html',{'serializer':serializer})
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data = request.POST)
        if serializer.is_valid():
                serializer.save()
                # Redirect to success page or show success message
                return render(request, 'login.html', {
                    'item': serializer.data,
                    'message': 'Account created successfully!'
                },status=status.HTTP_201_CREATED)
            
            # If invalid, re-render form with errors
        return render(request, 'register.html', {
                'serializer': serializer,
                'errors': serializer.errors,
                'form_data': request.POST  # To repopulate form
            }, status=status.HTTP_400_BAD_REQUEST)
# def register(request):
#     if request.method == 'POST':
#         name = request.POST.get('name','').strip()
#         email = request.POST.get('email','').strip()
#         phone = request.POST.get('phone').strip()
#         password = request.POST.get('password').strip()
#         confirm_password = request.POST.get('confirm_password').strip()

#         if not all([name,email,phone,password,confirm_password]):
#             messages.error(request,'All fields are Required')
#             return render(request,'register.html')
        
#         if password != confirm_password:
#             messages.error(request,'Passwords do not match')
#             return render(request,'register.html')
        
#         if len(password) < 8:
#             messages.error(request,'Password must be at least 8 characters long')
#             return render(request,'register.html')
#         if User.objects.filter(email=email).exists():
#             messages.error(request,'Email already exists')
#             return render(request,'register.html')
#         if User.objects.filter(username=name).exists():
#             messages.error(request, 'Username already exists')
#             return render(request, 'register.html')
        
#         try:
#             user = User.objects.create_user(
#                 username= name,
#                 email= email,
#                 password= password
#             )
#             user.phone = phone
#             user.save()

#             messages.success(request,'Account Created Successfully! You can now login!')
#             return redirect('login')
#         except Exception as e:
#             messages.error(request,f'Error creating account:{str(e)}')
#             return render(request,'register.html')
#     return render(request,'register.html')    


def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out successfully!')
    return redirect('home')



  
@login_required(login_url='login')

def dashboard(request):
    user_orders = WaterOrder.objects.filter(user=request.user)
    total_orders = user_orders.count()
    pending_orders = user_orders.filter(status='pending').count()
    recent_orders = user_orders.order_by('-order_date')[:5]

    context = {
        'total_orders':total_orders,
        'pending_orders':pending_orders,
        'recent_orders':recent_orders,
        'user':request.user
    }
    return render(request,'dashboard.html',context)

def buyWater(request):
    return render(request,'buy-water.html')
def admin(request):
    return render(request,'admin.html')
