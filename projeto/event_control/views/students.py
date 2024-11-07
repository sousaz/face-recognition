from django.shortcuts import render, HttpResponse
from event_control.forms.student import *
from event_control.forms.user import *

def register(request):
    studentForm = StudentForm()
    userForm = UserForm()
    return render(request, 'register_student.html', {'s_form':studentForm, 'u_form': userForm})