"""
URL configuration for projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from event_control.views import views, students, auth
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth
    path('', auth.login, name='login'),
    path('logout', auth.logout, name='logout'),
    # Student
    path('student/register/', students.register, name='register_student'),
    path('student/home/', students.home_student, name='home_student'),
    path('student/update/photo/', students.update_photo, name='update_photo'),
    path('student/profile/', students.profile, name='student_profile'),
    path("adm/home/", views.home_admin, name='adm_home'),
    path("adm/register-event/", views.register_event, name='register_event'),
    path('capture/', students.capture, name='capture'),
    path("__reload__/", include("django_browser_reload.urls")),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
