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
    promocoes,
    marcar_notificacao_lida,
    marcar_todas_notificacoes_lidas,
    minhas_reservas,
    minhas_solicitacoes,
    perfil,
    reservar_produto,
    solicitacoes,
    comercio,
    excluir_produto,
    avaliacoes,
    avaliar_produto,
    avaliar_estabelecimento,
    feedbacks_comercio,
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
    path("promocoes/", promocoes, name="promocoes"),
    path("promocoes/notificacao/<int:notificacao_id>/lida/", marcar_notificacao_lida, name="marcar_notificacao_lida"),
    path("promocoes/notificacoes/ler-todas/", marcar_todas_notificacoes_lidas, name="marcar_todas_notificacoes_lidas"),

    path("produtos/", index, name="produtos"),
    path("produto/<int:produto_id>/", detalhes_produto, name="detalhes_produto"),
    path("produto/<int:produto_id>/reservar/", reservar_produto, name="reservar_produto"),

    path("cadastro-produto/", cadastro_produto, name="cadastro_produto"),
    path("produto/<int:produto_id>/excluir/", excluir_produto, name="excluir_produto"),

    path("avaliacoes/", avaliacoes, name="avaliacoes"),
    path("avaliacoes/produto/<int:produto_id>/", avaliar_produto, name="avaliar_produto"),
    path("avaliacoes/estabelecimento/<int:estabelecimento_id>/", avaliar_estabelecimento, name="avaliar_estabelecimento"),
    path("feedbacks/", feedbacks_comercio, name="feedbacks_comercio"),

    path("comercio/", comercio, name="comercio"),
    path("solicitacoes/", minhas_solicitacoes, name="solicitacoes"),
    path("reserva/<int:reserva_id>/<str:status>/", atualizar_reserva, name="atualizar_reserva"),
    path("minhas-reservas/", minhas_reservas, name="minhas_reservas"),

    path("administrador/", admin_dashboard, name="administrador"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
