from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from .models import AccessKey, MicroFocusAdmin

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        User.objects.create_user(username=email, email=email, password=password)
        messages.success(request, 'Account created successfully.')
        return redirect('login')

    return render(request, 'registration/signup.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('access_keys')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'registration/login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')

        user = request.user
        user.set_password(password)
        user.save()
        messages.success(request, 'Password reset successfully.')
        return redirect('login')

    return render(request, 'registration/reset_password.html')

@login_required
def access_keys(request):
    keys = AccessKey.objects.filter(personnel=request.user)
    return render(request, 'access_keys.html', {'keys': keys})

@login_required
def revoke_key(request, key_id):
    key = AccessKey.objects.get(id=key_id)
    key.status = 'revoked'
    key.save()
    messages.success(request, 'Key revoked successfully.')
    return redirect('access_keys')

@login_required
def endpoint(request):
    if request.method == 'GET':
        email = request.GET.get('email', '')
        try:
            user = User.objects.get(username=email)
            key = AccessKey.objects.get(personnel=user, status='active')
            response = {
                'status': 200,
                'key_id': key.id,
                'expiry_date': key.expiry_date,
            }
        except (User.DoesNotExist, AccessKey.DoesNotExist):
            response = {
                'status': 404,
            }
        return JsonResponse(response)
