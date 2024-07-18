from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import tareaForm
from .models import Tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html',)

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #registro de usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tareas')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm, 
                    "error": 'Usuario existe'
                })
        return render(request, 'signup.html', {
                'form': UserCreationForm, 
                "error": 'Las contraseñas no coinciden'
        })

@login_required        
def tareas(request):
    tareas = Tarea.objects.filter(usuario=request.user, dia_completada__isnull=True)
    return render(request, 'tareas.html', {'tareas':tareas})

@login_required 
def signout(request):
    logout(request)
    return redirect('home')
 
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta' 
            })
        else:
            login(request, user)
            return redirect('tareas')

@login_required         
def create_tarea(request): 
    if request.method == 'GET':
        return render(request, 'create_tarea.html', {
            'form': tareaForm
        })
    else:
        try:
            form = tareaForm(request.POST)
            nueva_tarea = form.save(commit=False)
            nueva_tarea.usuario = request.user
            nueva_tarea.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'create_tarea.html', {
            'form': tareaForm,
            'error': 'Proporcionar datos validos'
        })

@login_required 
def tarea_detalle(request, tarea_id):

    if request.method == 'GET':
        task = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
        form = tareaForm(instance=task)
        return render (request, 'tarea_detalle.html',{
            'tarea': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
            form = tareaForm(request.POST, instance=task)
            form.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'tarea_detalle.html',{
            'tarea': task,
            'form': form,
            'error': "Error al actualizar tarea" 
            })

@login_required         
def completada(request, tarea_id):
    task = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        task.dia_completada = timezone.now()
        task.save()
        return redirect('tareas')

@login_required     
def eliminar(request, tarea_id):
    task = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tareas')

@login_required       
def tareas_completadas(request):
    tareas = Tarea.objects.filter(usuario=request.user, dia_completada__isnull=False).order_by('-dia_completada')
    return render(request, 'tareas.html', {
        'tareas':tareas
    })