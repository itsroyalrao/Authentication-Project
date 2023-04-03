from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login


# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        if username=='':
            messages.error(request, 'Invalid username')
            return redirect('/')

        elif email=='':
            messages.error(request, 'Invalid email')
            return redirect('/')

        elif password=='':
            messages.error(request, 'Invalid password')
            return redirect('/')

        elif password!=confirm_password:
            messages.error(request, 'Password do not match')
            return redirect('/')
        
        elif User.objects.filter(username=username):
            messages.error(request, 'Username is not available')
            return redirect('/')
        
        elif User.objects.filter(email=email):
            messages.error(request, 'Email is already registered')
            return redirect('/')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Your account has been succesfully created')
        return redirect('/signin/')
    
    return render(request, 'auth/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username is wrong!')
            return redirect('/signin/')

        if user is not None and user.check_password(password):
             login(request, user)
             return redirect('/home/')
        else:
            messages.error(request, 'Password is wrong')
            return redirect('/signin/')
        
    return render(request, 'auth/signin.html')

def signout(request):
    messages.success(request, 'Logout successfully!')
    return redirect('/signin/')

def home(request):
    return render(request, 'auth/home.html')