from django.conf import settings
from django.conf.urls.static import static
from django.urls import path



from . import views

urlpatterns = [
    path('',views.lista_carritos,name='lista_carritos'),
    path('ver_carrito/<int:id>/',views.ver_carrito, name="ver_carrito"),
    path('login/',views.login_view, name = 'login'),
    path('logout/',views.logout_view,name='logout'),
    path('registro/',views.registro,name ='registro'),
    path('crear_carritos/',views.crear_carrito,name="crear_carrito"),
    path('mis_carritos/',views.mis_carritos, name = 'mis_carritos'),
    path('mis_carritos/modificar_carrito/<int:id>/',views.modificar_carrito,name = 'modificar_carrito'),
    path('mapa/',views.mapa,name = 'mapa'),
    path('verificar/propietarios/',views.estado_propietarios,name = 'estado_propietarios'),
    path('verificar/propietarios/aceptar/<int:id>/',views.aceptar_propietario,name = 'aceptar_propietario'),
    path('verificar/propietarios/rechazar/<int:id>/',views.rechazar_propietario,name = 'rechazar_propietario'),
    path('verificar/carritos/',views.estado_carritos,name = 'estado_carritos'),
    path('verificar/carritos/aceptar/<int:id>/',views.aceptar_carrito,name = 'aceptar_carrito'),
    path('verificar/carritos/rechazar/<int:id>/',views.rechazar_carrito,name = 'rechazar_carrito'),
  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
