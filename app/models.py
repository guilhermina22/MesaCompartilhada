# Create your models here.

from django.db import models


class Usuario(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do usuário")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    senha = models.CharField(max_length=255, verbose_name="Senha")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class Estabelecimento(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name="Usuário"
    )
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    endereco = models.CharField(max_length=255, verbose_name="Endereço")

    def __str__(self):
        return self.usuario.nome

    class Meta:
        verbose_name = "Estabelecimento"
        verbose_name_plural = "Estabelecimentos"


class Consumidor(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name="Usuário"
    )

    def __str__(self):
        return self.usuario.nome

    class Meta:
        verbose_name = "Consumidor"
        verbose_name_plural = "Consumidores"


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


class Produto(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do produto")
    descricao = models.TextField(verbose_name="Descrição")
    precoOriginal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço"
    )
    quantidade = models.IntegerField(verbose_name="Quantidade")
    dataValidade = models.DateField(verbose_name="Data de validade")
    imagem = models.CharField(max_length=255, verbose_name="Imagem")
    status = models.CharField(max_length=30, verbose_name="Status")
    qtdEstoque = models.IntegerField(verbose_name="Quantidade em estoque")

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        verbose_name="Categoria"
    )

    estabelecimento = models.ForeignKey(
        Estabelecimento,
        on_delete=models.CASCADE,
        verbose_name="Estabelecimento"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


class Compra(models.Model):
    consumidor = models.ForeignKey(
        Consumidor,
        on_delete=models.CASCADE,
        verbose_name="Consumidor"
    )

    dataCompra = models.DateTimeField(verbose_name="Data da compra")
    valorTotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor total"
    )
    status = models.CharField(max_length=30, verbose_name="Status")

    def __str__(self):
        return f"Compra {self.id}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"


class ItemCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        verbose_name="Compra"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        verbose_name="Produto"
    )

    quantidade = models.IntegerField(verbose_name="Quantidade")
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


class AvaliacaoProduto(models.Model):
    consumidor = models.ForeignKey(
        Consumidor,
        on_delete=models.CASCADE,
        verbose_name="Consumidor"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        verbose_name="Produto"
    )

    nota = models.IntegerField(verbose_name="Nota")
    comentario = models.TextField(verbose_name="Comentário")
    dataAvaliacao = models.DateTimeField(verbose_name="Data da avaliação")

    def __str__(self):
        return f"Avaliação do produto {self.produto.nome}"

    class Meta:
        verbose_name = "Avaliação de Produto"
        verbose_name_plural = "Avaliações de Produtos"


class AvaliacaoEstabelecimento(models.Model):
    consumidor = models.ForeignKey(
        Consumidor,
        on_delete=models.CASCADE,
        verbose_name="Consumidor"
    )

    estabelecimento = models.ForeignKey(
        Estabelecimento,
        on_delete=models.CASCADE,
        verbose_name="Estabelecimento"
    )

    nota = models.IntegerField(verbose_name="Nota")
    comentario = models.TextField(verbose_name="Comentário")
    dataAvaliacao = models.DateTimeField(verbose_name="Data da avaliação")

    def __str__(self):
        return f"Avaliação de {self.estabelecimento.usuario.nome}"

    class Meta:
        verbose_name = "Avaliação de Estabelecimento"
        verbose_name_plural = "Avaliações de Estabelecimentos"