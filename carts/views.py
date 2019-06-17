
from builtins import object

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

from carts.models import Carrito, Perfil, Productos


def login_view(request):
    alert = 'verde'
    if request.method == 'POST':
        username = request.POST['txtuser'].lower()
        password = request.POST['txtpass']
        user = authenticate(request,username = username, password=password)
        if user:
            login(request,user)
            context = {'alert':alert}
            return HttpResponseRedirect(reverse('lista_carritos'))
        else:
            alert ='roja'
            messages.error(request,'Credenciales incorrectas')
            context = {'alert':alert}
            return render(request, 'carts/login.html',context)
    else:
        context = {'alert':alert}
        return render(request,'carts/login.html',context) 
@login_required(login_url='login')
def logout_view(request):
  
    if request.method == 'POST':
        logout(request)
    return redirect('login')

def registro(request):
    user = User()
    alert = 'verde' 
    if request.method == "POST":
        
            if request.POST.get('txttipo') == 'Propietario':
                try: 
                    user = User.objects.create_user(username=request.POST.get('txtemail'),password=request.POST.get('txtpass'),is_active=False)
                except:
                    messages.success(request,'Usuario ya registrado')
                    variabes = {'alert':alert} 
                    return render(request,'carts/registro.html',variabes)
            else:
                try:
                    user = User.objects.create_user(username=request.POST.get('txtemail'),password=request.POST.get('txtpass'))
                except:
                    alert = 'roja' 
                    messages.success(request,'Usuarioya registrado')
                    variabes = {'alert':alert} 
                    return render(request,'carts/registro.html',variabes)
            user.perfil.tipo = request.POST.get('txttipo')
            user.email = request.POST.get('txtemail')
            user.first_name = request.POST.get('txtnombre')
            user.last_name = request.POST.get('txtapellido')
            user.perfil.direccion = request.POST.get('txtdireccion')
            user.perfil.telefono = int(request.POST.get('txttelefono'))
            try:
                assign_role(user, 'propietario')
                user.save()
                messages.success(request,'Registro con exito espere su activacion')
                variabes = {'alert':alert} 
                return render(request,'carts/registro.html',variabes)
            except:
                alert = 'roja' 
                messages.success(request,'Los datos son incorrectos')
                variabes = {'alert':alert} 
                return render(request,'carts/registro.html',variabes)
       
    else:       
    
                
        variabes = {'alert':alert} 
        return render(request,'carts/registro.html',variabes)

def lista_carritos(request):
    carros = Carrito.objects.filter(estado='Aceptado')
    varibales = {'carros':carros}
    return render(request,'carts/lista_carritos.html',varibales)
@login_required(login_url='login')
def crear_carrito(request):
    alert = 'verde'
    if request.method == 'POST':
        cart = Carrito()
        cart.solicitante = request.user
        cart.nombre = request.POST.get('txtnombre')
        cart.longitud = float(request.POST.get('txtlongitud'))
        cart.latitud = float(request.POST.get('txtlatitud'))
        cart.imagen = request.FILES.get('txtimagen')
        cart.nombre_dueño = request.POST.get('txtnombredueño')
        cart.direccion = request.POST.get('txtdireccion')
        cart.descripcion = request.POST.get('txtdescripcion')
        try:
            cart.save()
            messages.success(request,'Carrito registrado y la espera')
            variables = {'alert':alert}
            return render(request,'carts/crear_carrito.html',variables)
        except  Exception as e:
            print('ERRRORR')
            print(type(e))
            alert = 'roja'
            messages.error(request,'Errror al registra carrito')
            variables = {'alert':alert}
            return render(request,'carts/crear_carrito.html',variables)
    else:
        variables = {'alert':alert}

        return render(request,'carts/crear_carrito.html')
@login_required(login_url='login')
def mis_carritos(request):
    if request.user.is_staff:
        carros = Carrito.objects.all()
    else:
        carros = Carrito.objects.filter(solicitante=request.user.pk)
    varibales = {'carros':carros}
    return render(request,'carts/mis_carritos.html',varibales)
@login_required(login_url='login')
def modificar_carrito(request,id):
    
    
    micarro = get_object_or_404(Carrito,id=id)
    productos = Productos.objects.filter(carritos=id)
    alert = 'verde'
    
    if request.method == 'POST' and 'btn-form-1' in request.POST:
        cart = Carrito()
        cart.id = request.POST.get('txtid')
        cart.solicitante = micarro.solicitante
        cart.nombre = request.POST.get('txtnombre')
        if request.FILES.get('txtimagen') is None:
            cart.imagen = micarro.imagen
        else:
            cart.imagen = request.FILES.get('txtimagen')
        cart.longitud =  float(request.POST.get('txtlongitud'))
        cart.latitud = float(request.POST.get('txtlatitud'))
        cart.nombre_dueño = request.POST.get('txtnombredueño')
        cart.direccion = request.POST.get('txtdireccion')
        cart.descripcion = request.POST.get('txtdescripcion')
        try:
            
            cart.save()
            messages.success(request,'Carrito modificado')
            
            return redirect('modificar_carrito',id=micarro.id)
        except Exception as e:
            print('Este es el error vergaasxd')
            print(type(e))
            alert = 'roja'
            messages.error(request,'Errror al modificar')
           
            return redirect('modificar_carrito',id=micarro.id)
    if  request.method == 'POST' and 'btn-form-2' in request.POST:
        producto = Productos()
        producto.carritos = micarro
        producto.nombre = request.POST.get('txtnombrepro')
        producto.imagen = request.FILES.get('txtimagenpro')
        producto.precio = int(request.POST.get('txtprecio'))
        producto.descripcion = request.POST.get('txtdescripcionpro')
        try:
            producto.save()
            messages.success(request,'Producto agregado')
            return redirect('modificar_carrito',id=micarro.id)
        except Exception as e:
            alert = 'roja'
            print('Este es el error vergaasxd')
            print(type(e))
            messages.success(request,'Error al agregar producto')
            return redirect('modificar_carrito',id=micarro.id)

    variables = {'alert':alert,
                'micarro':micarro,
                'productos':productos}
    print(productos)
    return render(request,'carts/modificar_carrito.html',variables)

def ver_carrito(request,id):
    carrito = get_object_or_404(Carrito,id=id)
    productos = Productos.objects.filter(carritos=id)
    variables = {'carrito':carrito,
                'productos':productos}
    return render(request,'carts/ver_carrito.html',variables)

def mapa(request):
    carros = Carrito.objects.all()
    variables = {'carros':carros}
    return render(request,'carts/mapa.html',variables)
@user_passes_test(lambda u:u.is_staff, login_url=('login'))  
def estado_propietarios(request):
    propietarios =  User.objects.filter(perfil__tipo="Propietario")
 
    variables = {'propietarios':propietarios}

    return render(request,'carts/estado_propietarios.html',variables)
@login_required(login_url='login')
def estado_carritos(request):
    if request.user.is_staff:
        carritos = Carrito.objects.all()
    else:
        carritos = Carrito.objects.filter(solicitante=request.user.pk)

    variables = {'carritos':carritos}
    return render(request,'carts/estado_carritos.html',variables)



@user_passes_test(lambda u:u.is_staff, login_url=('login'))  
def aceptar_propietario(request,id):
    pro = User.objects.filter(id=id)
    pro.update(is_active=True)
    return redirect('estado_propietarios')


@user_passes_test(lambda u:u.is_staff, login_url=('login'))  
def rechazar_propietario(request,id):
    pro = User.objects.filter(id=id)
    pro.update(is_active=False)
    return redirect('estado_propietarios')
@user_passes_test(lambda u:u.is_staff, login_url=('login'))  
def aceptar_carrito(request,id):
    cart = Carrito.objects.filter(id=id)
    cart.update(estado="Aceptado")
    return redirect('estado_carritos')
@user_passes_test(lambda u:u.is_staff, login_url=('login'))  
def rechazar_carrito(request,id):
    cart = Carrito.objects.filter(id=id)
    cart.update(estado="Rechazado")
    return redirect('estado_carritos')
