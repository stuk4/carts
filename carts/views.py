from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import request
from django.urls import reverse
from django.utils import timezone
from rolepermissions.checkers import has_role
from rolepermissions.roles import assign_role
from rolepermissions.utils import user_is_authenticated


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['txtuser'].lower()
        password = request.POST['txtpass']
        user = authenticate(request,username = username, password=password)
        if user:
            login(request,user)
            
            return HttpResponseRedirect(reverse('lista_carritos'))
        else:
            messages.error(request,'Credenciales incorrectas')

            return render(request, 'carts/login.html',context)
    else:
        return render(request,'carts/login.html',context) 
@login_required(login_url='login')
def logout_view(request):
  
    if request.method == 'POST':
        logout(request)
    return redirect('login')

def registro(request):
    user = User()
    if request.method == "POST":
        
        if request.POST.get('txttipo') == 'Propietario':
            
            user = User.objects.create_user(username=request.POST.get('txtemail'),password=request.POST.get('txtpass'),is_active=False)
            user.perfil.tipo = request.POST.get('txttipo')
            user.email = request.POST.get('txtemail')
            user.first_name = request.POST.get('txtnombre')
            user.last_name = request.POST.get('txtapellido')
            user.perfil.direccion = request.POST.get('txtdireccion')
            user.perfil.telefono = int(request.POST.get('txttelefono'))
            assign_role(user, 'propietario')
            user.save()
        else:
            user = User.objects.create_user(username=request.POST.get('txtemail'),password=request.POST.get('txtpass'))
            user.perfil.tipo = request.POST.get('txttipo')
            user.email = request.POST.get('txtemail')
            user.first_name = request.POST.get('txtnombre')
            user.last_name = request.POST.get('txtapellido')
            user.perfil.direccion = request.POST.get('txtdireccion')
            user.perfil.telefono = int(request.POST.get('txttelefono'))
        
            assign_role(user, 'propietario')
            user.save()
        return HttpResponseRedirect(reverse('inicio'))
    return render(request,'carts/registro.html')

def lista_carritos(request):
    return render(request,'carts/lista_carritos.html')
def crear_carrito(request):
    return render(request,'carts/crear_carrito.html')