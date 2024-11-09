from django.shortcuts import render, HttpResponse, redirect
from event_control.forms.student import *
from event_control.forms.user import *
import cv2
import threading
from django.views.decorators import gzip
from django.http import JsonResponse
import numpy as np
import base64

@gzip.gzip_page
def register(request):
    studentForm = StudentForm()
    userForm = UserForm()
    return render(request, 'register_student.html', {'s_form':studentForm, 'u_form': userForm})

def capture(request):
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