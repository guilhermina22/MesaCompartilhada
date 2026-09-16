from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app.views import (
    admin_dashboard,
    atualizar_reserva,
    cadastro_comerciante,
    cadastro_consumidor,
    cadastro_produto,
    conscientizacao,
    detalhes_produto,
    index,
    login,
    logout_view,
    mapa,
    minhas_reservas,
    minhas_solicitacoes,
    perfil,
    reservar_produto,
    solicitacoes,
    comercio,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),

    path("login/", login, name="login"),
    path("sair/", logout_view, name="logout"),

    path("cadastro/consumidor/", cadastro_consumidor, name="cadastro_consumidor"),
    path("cadastro/comerciante/", cadastro_comerciante, name="cadastro_comerciante"),

    path("perfil/", perfil, name="perfil"),
    path("conscientizacao/", conscientizacao, name="conscientizacao"),
    path("mapa/", mapa, name="mapa"),

    path("produtos/", index, name="produtos"),
    path("produto/<int:produto_id>/", detalhes_produto, name="detalhes_produto"),
    path("produto/<int:produto_id>/reservar/", reservar_produto, name="reservar_produto"),

    path("cadastro-produto/", cadastro_produto, name="cadastro_produto"),

    path("comercio/", comercio, name="comercio"),
    path("solicitacoes/", minhas_solicitacoes, name="solicitacoes"),
    path("reserva/<int:reserva_id>/<str:status>/", atualizar_reserva, name="atualizar_reserva"),
    path("minhas-reservas/", minhas_reservas, name="minhas_reservas"),

    path("administrador/", admin_dashboard, name="administrador"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
