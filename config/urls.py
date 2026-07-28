from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Página inicial
    path("", views.index, name="index"),

    # Login
    path("login/", views.login_view, name="login"),

    # Cadastros
    path("cadastro/consumidor/", views.cadastro_consumidor, name="cadastro_consumidor"),
    path("cadastro/comerciante/", views.cadastro_comerciante, name="cadastro_comerciante"),

    # Painéis
    path("home/", views.home, name="home"),
    path("perfil/", views.perfil, name="perfil"),
    path("produtos/", views.produtos, name="produtos"),
    path("conscientizacao/", views.conscientizacao, name="conscientizacao"),
]