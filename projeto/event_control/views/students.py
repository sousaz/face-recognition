from django.shortcuts import render, redirect
from event_control.forms.student import *
from event_control.forms.user import *
import base64
from django.contrib.auth.models import Group
from django.http import HttpResponse

def register(request):
    if request.method == 'GET':
        studentForm = StudentForm()
        userForm = UserForm()
    elif request.method == 'POST':
        studentForm = StudentForm(request.POST, request.FILES)
        userForm = UserForm(request.POST)
        if studentForm.is_valid() and userForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()
            group = Group.objects.get(name="student")
            user.groups.add(group)
            student = studentForm.save(commit=False)
            student.user_id = user
            student.save()
            return redirect('login')
    context = {
        's_form':studentForm,
        'u_form': userForm,
        'title': 'Cadastro'
    }
    return render(request, 'register_student.html', context)

def home_student(request):
    student = Student.objects.filter(user_id=request.user).get()
    context = {
        'title': 'Home',
        'student': student
    }
    return render(request, 'home_student.html', context)

def update_photo(request):
    student = Student.objects.filter(user_id=request.user).first()
    if request.method == 'GET':
        form = UpdatePhotoForm(instance=student)
    elif request.method == 'POST':
        form = UpdatePhotoForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            print("Foto recebida:", request.FILES.get('photo'))
            form.save()
            return redirect('home_student')
    context = {
        'title': 'Atualizar foto',
        'form': form,
    }
    return render(request, 'update_photo.html', context)

def capture(request):
    return HttpResponse(request.user.get_all_permissions())
    if request.method == 'POST':
        foto_data = request.POST.get('foto_data')

        if foto_data:
            # Remover o prefixo "data:image/jpeg;base64,"
            format, img_str = foto_data.split(';base64,') 
            img_data = base64.b64decode(img_str)

            # Criar a imagem e salvar no banco de dados
            # image_file = ContentFile(img_data, 'captura.jpg')
            # foto = Foto(imagem=image_file)
            # foto.save()

            # Redirecionar para a página de detalhes da foto
            return redirect('teste')

    return render(request, 'capture.html')