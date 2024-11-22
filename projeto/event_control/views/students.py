from django.shortcuts import render, redirect
from event_control.forms.student import *
from event_control.forms.user import *
from django.contrib.auth.models import Group
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from django.utils.timezone import localtime
import os
from django.conf import settings

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
    certificates = Certificate.objects.filter(student_id=student).all()

    context = {
        'title': 'Home',
        'student': student,
        'certificates': certificates
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

def download_certificate(request, id):
    certificate = Certificate.objects.filter(id=id).first()
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
    p.drawCentredString(largura / 2, altura - 200, certificate.student_id.name)

    p.setFont("Helvetica", 12)
    p.setFillColor(colors.HexColor("#00539C"))
    p.drawCentredString(largura / 2, altura - 220, f"Matriculado no curso de {certificate.student_id.course}")

    # Adicionar a frase principal
    p.setFont("Helvetica", 16)
    p.setFillColor(colors.black)
    texto_evento = f"Participou do evento {certificate.event_id.name}"

    texto_carga_horaria = f"Carga horária: {certificate.event_id.workload.hour} horas e {certificate.event_id.workload.minute} minutos."

    # Adicionar a linha com o evento
    p.drawCentredString(largura / 2, altura - 250, texto_evento)

    # Adicionar a carga horária na linha de baixo
    p.setFont("Helvetica", 14)
    p.setFillColor(colors.black)
    p.drawCentredString(largura / 2, altura - 270, texto_carga_horaria)

    # Adicionar a data
    p.setFont("Helvetica-Oblique", 12)
    p.setFillColor(colors.black)
    formatted_date = localtime(certificate.event_id.start_date).strftime('%d/%m/%Y %H:%M')
    p.drawCentredString(largura / 2, altura - 310, f"Data do evento: {formatted_date}")

    # Adicionar a assinatura (simulada)
    signature = Signature.objects.first()
    signature_path = os.path.join(settings.MEDIA_ROOT, signature.signature_image.name)
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawImage(signature_path, 140, 95, width=80, height=80, mask="auto")
    p.drawString(100, 100, "_________________________")
    p.drawString(100, 85, "Assinatura do Diretor")

    # Finalizar o PDF
    p.showPage()
    p.save()

    return response