from django.shortcuts import render, redirect
from event_control.forms.student import *
from event_control.forms.user import *
import base64
from django.contrib.auth.models import Group
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from django.utils.timezone import localtime
import os
from django.conf import settings
import face_recognition as fr
import cv2
from django.contrib import messages
import numpy as np
from io import BytesIO
import json

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
    register = Register.objects.filter(student_id=student).all()
    result = []
    for r in register:
        if r.computed:
            result.append(r)
            continue
        if r.event_id.register_type == 'eo' and r.check_in >= r.event_id.start_date:
            end_of_day = r.event_id.start_date.replace(hour=23, minute=59, second=59)
            if r.check_in <= end_of_day:
                result.append(r)
        if r.event_id.register_type == 'ee' and r.check_in and r.check_out:
            if r.check_in >= r.event_id.start_date and r.check_out <= r.event_id.end_date:
                result.append(r)
        r.computed = True
        r.save()

    context = {
        'title': 'Home',
        'student': student,
        'register': result
    }
    return render(request, 'home_student.html', context)

def update_photo(request):
    student = Student.objects.filter(user_id=request.user).first()
    if request.method == 'GET':
        form = UpdatePhotoForm(instance=student)
    elif request.method == 'POST':
        form = UpdatePhotoForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('home_student')
    context = {
        'title': 'Atualizar foto',
        'form': form,
    }
    return render(request, 'update_photo.html', context)

def profile(request):
    student = Student.objects.filter(user_id=request.user).first()
    form = ProfileForm(instance=student)
    context = {
        'title': 'Meu Perfil',
        'form': form,
    }
    return render(request, 'profile.html', context)

def capture(request):
    if request.method == 'POST':
        image_data = request.POST.get('face_image')

        if image_data:
            # Remover o prefixo 'data:image/png;base64,' da string base64
            image_data = image_data.split(',')[1]

            # Decodificar a string base64 para obter os dados binários da imagem
            image_binary = base64.b64decode(image_data)

            image_file = BytesIO(image_binary)

            # try:
            img = fr.load_image_file(image_file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = fr.face_encodings(img)[0]
            students = Student.objects.all()
            for s in students:
                matches = fr.compare_faces([json.loads(s.photo_encoding)], encode)
                if matches[0] == True:
                    messages.success(request, f'Tudo certo, {s.name}')
                    return render(request, 'capture.html')
            messages.error(request, "Algo deu errado")

    return render(request, 'capture.html')

def download_certificate(request, id):
    register = Register.objects.filter(id=id).first()
    largura, altura = landscape(A4)  # Alterar para folha deitada

    # Criar o objeto de resposta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado.pdf"'

    # Criar o canvas do certificado
    p = canvas.Canvas(response, pagesize=landscape(A4))

    # Desenhar uma borda ao redor do certificado
    p.setStrokeColor(colors.HexColor("#00539C"))
    p.setLineWidth(4)
    p.rect(30, 30, largura - 60, altura - 60)

    # Adicionar o cabeçalho do certificado
    p.setFont("Helvetica-Bold", 28)
    p.setFillColor(colors.HexColor("#00539C"))
    p.drawCentredString(largura / 2, altura - 100, "CERTIFICADO DE CONCLUSÃO")

    # Adicionar uma linha de descrição
    p.setFont("Helvetica", 16)
    p.setFillColor(colors.black)
    p.drawCentredString(
        largura / 2,
        altura - 150,
        "Declaro que o discente:",
    )

    # Adicionar o nome do participante em destaque
    p.setFont("Helvetica-Bold", 22)
    p.setFillColor(colors.HexColor("#00539C"))
    p.drawCentredString(largura / 2, altura - 200, register.student_id.name)

    p.setFont("Helvetica", 12)
    p.setFillColor(colors.HexColor("#00539C"))
    p.drawCentredString(largura / 2, altura - 220, f"Matriculado no curso de {register.student_id.course}")

    # Adicionar a frase principal
    p.setFont("Helvetica", 16)
    p.setFillColor(colors.black)
    texto_evento = f"Participou do evento {register.event_id.name}"

    formatted_check_in = localtime(register.check_in)
    formatted_check_out = localtime(register.check_out)
    diference = (formatted_check_out - formatted_check_in)
    total_seconds = diference.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    texto_carga_horaria = f"Carga horária: {hours} horas e {minutes} minutos."

    # Adicionar a linha com o evento
    p.drawCentredString(largura / 2, altura - 250, texto_evento)

    # Adicionar a carga horária na linha de baixo
    p.setFont("Helvetica", 14)
    p.setFillColor(colors.black)
    p.drawCentredString(largura / 2, altura - 270, texto_carga_horaria)

    # Adicionar a data
    p.setFont("Helvetica-Oblique", 12)
    p.setFillColor(colors.black)
    formatted_date = localtime(register.event_id.start_date).strftime('%d/%m/%Y %H:%M')
    p.drawCentredString(largura / 2, altura - 310, f"Data do evento: {formatted_date}")

    # Adicionar a assinatura (simulada)
    signature_path = os.path.join(settings.MEDIA_ROOT, 'img', 'assinatura.png')
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawImage(signature_path, 140, 95, width=80, height=80, mask="auto")
    p.drawString(100, 100, "_________________________")
    p.drawString(100, 85, "Assinatura do Diretor")

    # Finalizar o PDF
    p.showPage()
    p.save()

    return response