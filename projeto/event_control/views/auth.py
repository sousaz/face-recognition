from django.shortcuts import render, redirect, HttpResponse
from event_control.forms.user import *
from django.contrib.auth import authenticate, login as loginUser, logout as lgt
from django.contrib import messages

def login(request):
    if request.method == 'GET':
        form = UserAuthForm()
    elif request.method == 'POST':
        form = UserAuthForm(request.POST)

        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                loginUser(request, user)
                if user.groups.filter(name='admin').exists():
                    return redirect('adm_home')
                return redirect('home_student')
        messages.error(request, 'Credenciais incorretas, tente novamente!')

    context = {
        'title': 'Login',
        'form': form
    }
    return render(request, 'login.html', context)

def logout(request):
    lgt(request)
    return redirect('login')