from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url

from cart.models import Item, Cart


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            try:
                user = User.objects.get(username=request.POST['name'])
                return render(request, 'accounts/signup.html', {'User already existed...'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                        username=request.POST['name'], email=request.POST['email'], password=request.POST['password']
                )
                next_ = request.POST.get('next')
                auth.login(request, user)
                if is_safe_url(next_, request.get_host()):
                    return redirect(next_)
                else:
                    return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Password must match...'})
    else:
        return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['name'], password=request.POST['password'])
        next_ = request.POST.get('next')
        if user is not None:
            auth.login(request, user)
            if is_safe_url(next_, request.get_host()):
                return redirect(next_)
            else:
                return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Email or Password is incorrect...'})
    else:
        return render(request, 'accounts/login.html')


@login_required
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        Item.objects.all().delete()
        Cart.objects.all().delete()
        return render(request, 'accounts/logout.html')
