from django.contrib import admin
from django.urls import path
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('login/', login, name='login'),
    path('cadastro/consumidor/', cadastro_consumidor, name='cadastro_consumidor'),
    path('cadastro/comerciante/', cadastro_comerciante, name='cadastro_comerciante'),
    path('home/', home, name='home'),
    path('perfil/', perfil, name='perfil'),
    path('produtos/', produtos, name='produtos'),
    path('conscientizacao/', conscientizacao, name='conscientizacao'),

    path('mapa/', mapa, name='mapa'),
    path('detalhes_doacao/', detalhes_doacao, name='detalhes_doacao'),
        path('explorar_doacoes/', explorar_doacoes, name='explorar_doacoes'),
    path('cadastro_doacao/', cadastro_doacao, name='cadastro_doacao'),
    path('comercio/', comercio, name='comercio'),
    path('solicitacoes/', solicitacoes, name='solicitacoes'),
    path('administrador/', admin_dashboard, name='administrador'),
]