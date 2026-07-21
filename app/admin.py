from django.contrib import admin
from .models import *

admin.site.register(Usuario)
admin.site.register(Consumidor)
admin.site.register(Estabelecimento)
admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Compra)
admin.site.register(ItemCompra)
admin.site.register(AvaliacaoProduto)
admin.site.register(AvaliacaoEstabelecimento)
