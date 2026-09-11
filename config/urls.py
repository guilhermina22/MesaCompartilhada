from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app.views import (
    index,
    login,
    cadastro_consumidor,
    cadastro_comerciante,
    perfil,
    conscientizacao,
    mapa,
    explorar_doacoes,
    detalhes_doacao,
    cadastro_doacao,
    comercio,
    solicitacoes,
    admin_dashboard,
)


urlpatterns = [

    # =========================
    # ADMIN DO DJANGO
    # =========================

    path(
        "admin/",
        admin.site.urls
    ),


    # =========================
    # PÁGINA INICIAL
    # =========================

    path(
        "",
        index,
        name="index"
    ),


    # =========================
    # LOGIN
    # =========================

    path(
        "login/",
        login,
        name="login"
    ),


    # =========================
    # CADASTROS
    # =========================

    path(
        "cadastro/consumidor/",
        cadastro_consumidor,
        name="cadastro_consumidor"
    ),

    path(
        "cadastro/comerciante/",
        cadastro_comerciante,
        name="cadastro_comerciante"
    ),


    # =========================
    # PERFIL
    # =========================

    path(
        "perfil/",
        perfil,
        name="perfil"
    ),


    # =========================
    # CONSCIENTIZAÇÃO
    # =========================

    path(
        "conscientizacao/",
        conscientizacao,
        name="conscientizacao"
    ),


    # =========================
    # MAPA
    # =========================

    path(
        "mapa/",
        mapa,
        name="mapa"
    ),


    # =========================
    # DOAÇÕES
    # =========================

    path(
        "explorar_doacoes/",
        explorar_doacoes,
        name="explorar_doacoes"
    ),

    path(
        "detalhes_doacao/",
        detalhes_doacao,
        name="detalhes_doacao"
    ),

    path(
        "cadastro_doacao/",
        cadastro_doacao,
        name="cadastro_doacao"
    ),


    # =========================
    # COMÉRCIO
    # =========================

    path(
        "comercio/",
        comercio,
        name="comercio"
    ),


    # =========================
    # SOLICITAÇÕES
    # =========================

    path(
        "solicitacoes/",
        solicitacoes,
        name="solicitacoes"
    ),


    # =========================
    # ADMINISTRADOR
    # =========================

    path(
        "administrador/",
        admin_dashboard,
        name="administrador"
    ),

]


# =========================
# ARQUIVOS DE MÍDIA
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )