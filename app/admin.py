from django.contrib import admin
from .models import *


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "telefone")
    search_fields = ("nome", "email", "telefone")
    ordering = ("nome",)


@admin.register(Consumidor)
class ConsumidorAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario")
    search_fields = ("usuario__nome", "usuario__email")


@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "descricao", "endereco")
    search_fields = (
        "usuario__nome",
        "usuario__email",
        "descricao",
        "endereco",
    )


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nomeCategoria")
    search_fields = ("nomeCategoria",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "categoria",
        "estabelecimento",
        "precoOriginal",
        "quantidade",
        "status",
    )

    list_filter = (
        "categoria",
        "status",
        "estabelecimento",
    )

    search_fields = (
        "nome",
        "descricao",
    )

    ordering = ("nome",)


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "consumidor",
        "valorTotal",
        "status",
        "dataCompra",
    )

    list_filter = (
        "status",
        "dataCompra",
    )

    search_fields = (
        "consumidor__usuario__nome",
    )


@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "compra",
        "produto",
        "quantidade",
        "precoUnitario",
        "subtotal",
    )

    search_fields = (
        "produto__nome",
    )


@admin.register(AvaliacaoProduto)
class AvaliacaoProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "produto",
        "consumidor",
        "nota",
        "dataAvaliacao",
    )

    list_filter = (
        "nota",
    )

    search_fields = (
        "produto__nome",
        "consumidor__usuario__nome",
    )


@admin.register(AvaliacaoEstabelecimento)
class AvaliacaoEstabelecimentoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "estabelecimento",
        "consumidor",
        "nota",
        "dataAvaliacao",
    )

    list_filter = (
        "nota",
    )

    search_fields = (
        "estabelecimento__usuario__nome",
        "consumidor__usuario__nome",
    )