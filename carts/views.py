
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

from carts.models import Carrito,Productos


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
                assign_role(user, 'normal')
                user.save()
                messages.success(request,'Registrado como usuario normal')
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
    carros = Carrito.objects.all()
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
        cart.longitud = micarro.longitud
        cart.latitud = micarro.latitud
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
    variables = {'carrito':carrito}
    return render(request,'carts/ver_carrito.html',variables)



    ##ME FALTA AGREGAR PRODUTOS A UN CARRITO QUE NO PUEDOD HACERLO EN UN MISMO TEMPALTE T_T