from django.shortcuts import render, HttpResponse
import cv2
import face_recognition as fr

def home_admin(request):
    return render(request, 'home_admin.html')

def register_event(request):
    return render(request, 'register_event.html')

# Create your views here.
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