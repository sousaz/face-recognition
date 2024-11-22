from django.shortcuts import render, HttpResponse, redirect
from event_control.forms.event import *
from django.db.models import Q
from django.contrib import messages
import cv2
import face_recognition as fr
from io import BytesIO
import json
import base64

# Create your views here.
def home_admin(request):
    events = Event.objects.all()
    if request.method == 'POST':
        search = request.POST.get('search')
        events = events.filter(Q(name__icontains=search) | Q(start_date__icontains=search))
    context = {
        'title': 'Home',
        'events': events
    }
    return render(request, 'home_admin.html', context)

def register_event(request):
    if request.method == 'GET':
        form = EventForm()
    elif request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adm_home')
    context = {
        'title': 'Registro de eventos',
        'form': form
    }
    return render(request, 'register_event.html', context)

def event_details(request, id):
    event = Event.objects.filter(id=id).first()
    if request.method == 'GET':
        form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('adm_home')
    context = {
        'title': 'Detalhes do evento',
        'form': form,
    }
    return render(request, 'event_details.html', context)

def delete_event(request, id):
    register = Register.objects.filter(event_id=id).exists()
    if register:
        messages.error(request, 'Não é possivel apagar eventos que ja teve algum registro')
        return redirect('adm_home')
    Event.objects.filter(id=id).delete()
    messages.success(request, 'Evento apagado com sucesso')
    return redirect('adm_home')

def event_participants(request, id):
    register = Register.objects.filter(event_id=id).all()
    context = {
        'title': 'Participantes',
        'register': register
    }
    return render(request, 'event_participants.html', context)

def generate_certificates(request, id):
    register = Register.objects.filter(event_id=id, computed=False).all()
    if register:
        if register[0].event_id.register_type == 'eo':
            for r in register:
                if r.check_in >= r.event_id.start_date and r.check_in <= r.event_id.end_date:
                    Certificate(student_id=r.student_id, event_id=r.event_id).save()
                r.computed = True
                r.save()
        else:
            for r in register:
                if r.check_in >= r.event_id.start_date and r.check_out <= r.event_id.end_date:
                    difference_in_hours = (r.check_out - r.check_in).total_seconds() / 3600
                    min_hours_in_float = r.event_id.min_hours.hour + r.event_id.min_hours.minute / 60
                    if difference_in_hours >= min_hours_in_float:
                        Certificate(student_id=r.student_id, event_id=r.event_id).save()
                r.computed = True
                r.save()


    return redirect('adm_home')

def capture(request, id):
    if request.method == 'POST':
        image_data = request.POST.get('face_image')

        if image_data:
            image_data = image_data.split(',')[1]

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

def teste(request):
    if request.method == 'GET':
        return render(request, 'teste.html')
    elif request.method == 'POST':
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')

        img = fr.load_image_file(img1)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        imgTest = fr.load_image_file(img2)
        imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)

        faceLoc = fr.face_locations(img)[0]
        cv2.rectangle(img,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(0,255,0),2)

        encode = fr.face_encodings(img)[0]
        encodeTest = fr.face_encodings(imgTest)[0]

        comparacao = fr.compare_faces([encode],encodeTest)
        distancia = fr.face_distance([encode],encodeTest)

        return HttpResponse(comparacao,distancia)