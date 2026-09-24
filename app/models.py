from django.db import models


# =========================================================
# USUÁRIO
# =========================================================

class Usuario(models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do usuário"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="E-mail"
    )

    senha = models.CharField(
        max_length=255,
        verbose_name="Senha"
    )

    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone"
    )

    cidade = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Cidade"
    )

    biografia = models.TextField(
        max_length=300,
        blank=True,
        verbose_name="Biografia"
    )

    foto_perfil = models.ImageField(
        upload_to="perfis/",
        blank=True,
        null=True,
        verbose_name="Foto de perfil"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
    



# =========================================================
# ESTABELECIMENTO
# =========================================================

class Estabelecimento(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="estabelecimento",
        verbose_name="Usuário"
    )

    descricao = models.CharField(
        max_length=255,
        verbose_name="Descrição"
    )

    endereco = models.CharField(
        max_length=255,
        verbose_name="Endereço"
    )

    def __str__(self):
        return self.usuario.nome

    class Meta:
        verbose_name = "Estabelecimento"
        verbose_name_plural = "Estabelecimentos"


# =========================================================
# CONSUMIDOR
# =========================================================

class Consumidor(models.Model):

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="consumidor",
        verbose_name="Usuário"
    )

    def __str__(self):
        return self.usuario.nome

    class Meta:
        verbose_name = "Consumidor"
        verbose_name_plural = "Consumidores"


# =========================================================
# CATEGORIA
# =========================================================

class Categoria(models.Model):

    nomeCategoria = models.CharField(
        max_length=100,
        verbose_name="Nome da categoria"
    )

    def __str__(self):
        return self.nomeCategoria

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


# =========================================================
# PRODUTO
# =========================================================

class Produto(models.Model):

    nome = models.CharField(
        max_length=100,
        verbose_name="Nome do produto"
    )

    descricao = models.TextField(
        verbose_name="Descrição"
    )

    precoOriginal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço original"
    )

    precoPromocional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Preço promocional"
    )

    quantidade = models.IntegerField(
        verbose_name="Quantidade"
    )

    dataValidade = models.DateField(
        verbose_name="Data de validade"
    )

    imagem = models.ImageField(
        upload_to="produtos/",
        blank=True,
        null=True,
        verbose_name="Imagem"
    )

    status = models.CharField(
        max_length=30,
        verbose_name="Status"
    )

    qtdEstoque = models.IntegerField(
        verbose_name="Quantidade em estoque"
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="produtos",
        verbose_name="Categoria"
    )

    estabelecimento = models.ForeignKey(
        Estabelecimento,
        on_delete=models.CASCADE,
        related_name="produtos",
        verbose_name="Estabelecimento"
    )

    @property
    def preco_venda(self):
        return self.precoPromocional if self.precoPromocional is not None else self.precoOriginal

    @property
    def desconto_percentual(self):
        if self.precoPromocional is None or not self.precoOriginal or self.precoPromocional >= self.precoOriginal:
            return 0
        return round((1 - (self.precoPromocional / self.precoOriginal)) * 100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


# =========================================================
# COMPRA
# =========================================================

class Compra(models.Model):

    consumidor = models.ForeignKey(
        Consumidor,
        on_delete=models.CASCADE,
        related_name="compras",
        verbose_name="Consumidor"
    )

    dataCompra = models.DateTimeField(
        verbose_name="Data da compra"
    )

    valorTotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor total"
    )

    status = models.CharField(
        max_length=30,
        verbose_name="Status"
    )

    def __str__(self):
        return f"Compra {self.id}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"


# =========================================================
# ITEM DA COMPRA
# =========================================================

class ItemCompra(models.Model):

    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name="itens",
        verbose_name="Compra"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="itens_compra",
        verbose_name="Produto"
    )

    quantidade = models.IntegerField(
        verbose_name="Quantidade"
    )

    precoUnitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço unitário"
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Subtotal"
    )

    def __str__(self):
        return f"Item {self.id}"

    class Meta:
        verbose_name = "Item da Compra"
        verbose_name_plural = "Itens da Compra"


# =========================================================
# AVALIAÇÃO DO PRODUTO
# =========================================================

class AvaliacaoProduto(models.Model):

    consumidor = models.ForeignKey(
        Consumidor,
        on_delete=models.CASCADE,
        related_name="avaliacoes_produtos",
        verbose_name="Consumidor"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="avaliacoes",
        verbose_name="Produto"
    )

    nota = models.IntegerField(
        verbose_name="Nota"
    )

    comentario = models.TextField(
        verbose_name="Comentário"
    )

    dataAvaliacao = models.DateTimeField(
        verbose_name="Data da avaliação"
    )

    def __str__(self):
        return f"Avaliação do produto {self.produto.nome}"

    class Meta:
        verbose_name = "Avaliação de Produto"
        verbose_name_plural = "Avaliações de Produtos"


# =========================================================
# AVALIAÇÃO DO ESTABELECIMENTO
# =========================================================

class AvaliacaoEstabelecimento(models.Model):

    consumidor = models.ForeignKey(
        Consumidor,
        on_delete=models.CASCADE,
        related_name="avaliacoes_estabelecimentos",
        verbose_name="Consumidor"
    )

    estabelecimento = models.ForeignKey(
        Estabelecimento,
        on_delete=models.CASCADE,
        related_name="avaliacoes",
        verbose_name="Estabelecimento"
    )

    nota = models.IntegerField(
        verbose_name="Nota"
    )

    comentario = models.TextField(
        verbose_name="Comentário"
    )

    dataAvaliacao = models.DateTimeField(
        verbose_name="Data da avaliação"
    )

    def __str__(self):
        return f"Avaliação de {self.estabelecimento.usuario.nome}"

    class Meta:
        verbose_name = "Avaliação de Estabelecimento"
        verbose_name_plural = "Avaliações de Estabelecimentos"

# =========================================================
# RESERVA DE PRODUTO
# =========================================================

class Reserva(models.Model):

    consumidor = models.ForeignKey(
        Consumidor,
        on_delete=models.CASCADE,
        related_name="reservas",
        verbose_name="Consumidor"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="reservas",
        verbose_name="Produto"
    )

    quantidade = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantidade"
    )

    dataReserva = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da reserva"
    )

    status = models.CharField(
        max_length=30,
        default="Pendente",
        verbose_name="Status"
    )

    def __str__(self):
        return f"Reserva {self.id} - {self.produto.nome}"

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

# =========================================================
# NOTIFICAÇÃO DE NOVA PROMOÇÃO
# =========================================================

class NotificacaoPromocao(models.Model):
    consumidor = models.ForeignKey(
        Consumidor,
        on_delete=models.CASCADE,
        related_name="notificacoes_promocao",
        verbose_name="Consumidor",
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="notificacoes_promocao",
        verbose_name="Produto",
    )
    lida = models.BooleanField(default=False, verbose_name="Lida")
    criadaEm = models.DateTimeField(auto_now_add=True, verbose_name="Criada em")

    def __str__(self):
        return f"Nova promoção: {self.produto.nome}"

    class Meta:
        verbose_name = "Notificação de promoção"
        verbose_name_plural = "Notificações de promoções"
        ordering = ["-criadaEm"]
        constraints = [
            models.UniqueConstraint(
                fields=["consumidor", "produto"],
                name="notificacao_unica_consumidor_produto",
            )
        ]

# =========================================================
# NOTIFICAÇÃO DE NOVA AVALIAÇÃO PARA O COMERCIANTE
# =========================================================
class NotificacaoAvaliacao(models.Model):
    estabelecimento = models.ForeignKey(
        Estabelecimento, on_delete=models.CASCADE,
        related_name="notificacoes_avaliacao", verbose_name="Estabelecimento"
    )
    avaliacao_produto = models.ForeignKey(
        AvaliacaoProduto, on_delete=models.CASCADE, null=True, blank=True,
        related_name="notificacoes_comerciante", verbose_name="Avaliação de produto"
    )
    avaliacao_estabelecimento = models.ForeignKey(
        AvaliacaoEstabelecimento, on_delete=models.CASCADE, null=True, blank=True,
        related_name="notificacoes_comerciante", verbose_name="Avaliação do estabelecimento"
    )
    lida = models.BooleanField(default=False, verbose_name="Lida")
    criadaEm = models.DateTimeField(auto_now_add=True, verbose_name="Criada em")

    def __str__(self):
        return f"Nova avaliação para {self.estabelecimento.usuario.nome}"

    class Meta:
        ordering = ["-criadaEm"]
        verbose_name = "Notificação de avaliação"
        verbose_name_plural = "Notificações de avaliações"
