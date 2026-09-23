from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CadastroComercianteForm,
    CadastroConsumidorForm,
    EstabelecimentoForm,
    LoginForm,
    ProdutoForm,
)
from .models import Categoria, Consumidor, Estabelecimento, Produto, Reserva, Usuario


def usuario_atual(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return None
    try:
        return Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        request.session.flush()
        return None


def exigir_login(request):
    usuario = usuario_atual(request)
    if usuario is None:
        return redirect("login")
    return usuario


def index(request):
    busca = request.GET.get("busca", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    preco = request.GET.get("preco", "").strip()

    produtos = Produto.objects.select_related(
        "estabelecimento",
        "estabelecimento__usuario",
        "categoria"
    ).filter(qtdEstoque__gt=0).order_by("-id")

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) |
            Q(estabelecimento__usuario__nome__icontains=busca)
        )

    if categoria:
        produtos = produtos.filter(categoria__nomeCategoria__iexact=categoria)

    if preco:
        try:
            produtos = produtos.filter(precoOriginal__lte=float(preco))
        except (ValueError, TypeError):
            pass

    categorias = Categoria.objects.all().order_by("nomeCategoria")

    return render(request, "index.html", {
        "produtos": produtos,
        "categorias": categorias,
        "busca": busca,
        "categoria": categoria,
        "preco": preco,
    })


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]

            try:
                usuario = Usuario.objects.get(email=email)
            except Usuario.DoesNotExist:
                usuario = None

            if usuario and usuario.senha == senha:
                request.session["usuario_id"] = usuario.id
                if hasattr(usuario, "estabelecimento"):
                    return redirect("comercio")
                return redirect("index")

            form.add_error(None, "E-mail ou senha incorretos.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    request.session.flush()
    return redirect("index")


def cadastro_consumidor(request):
    if request.method == "POST":
        form = CadastroConsumidorForm(request.POST)
        if form.is_valid():
            if Usuario.objects.filter(email=form.cleaned_data["email"]).exists():
                form.add_error("email", "Este e-mail já está cadastrado.")
            else:
                usuario = form.save(commit=False)
                usuario.senha = form.cleaned_data["senha"]
                usuario.save()
                Consumidor.objects.create(usuario=usuario)
                request.session["usuario_id"] = usuario.id
                return redirect("index")
    else:
        form = CadastroConsumidorForm()
    return render(request, "cadastro_consumidor.html", {"form": form})


def cadastro_comerciante(request):
    if request.method == "POST":
        form = CadastroComercianteForm(request.POST)
        estabelecimento_form = EstabelecimentoForm(request.POST)

        if form.is_valid() and estabelecimento_form.is_valid():
            if Usuario.objects.filter(email=form.cleaned_data["email"]).exists():
                form.add_error("email", "Este e-mail já está cadastrado.")
            else:
                usuario = form.save(commit=False)
                usuario.senha = form.cleaned_data["senha"]
                usuario.save()

                estabelecimento = estabelecimento_form.save(commit=False)
                estabelecimento.usuario = usuario
                estabelecimento.save()

                request.session["usuario_id"] = usuario.id
                return redirect("comercio")
    else:
        form = CadastroComercianteForm()
        estabelecimento_form = EstabelecimentoForm()

    return render(request, "cadastro_comerciante.html", {
        "form": form,
        "estabelecimento_form": estabelecimento_form,
    })


def perfil(request):
    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    if request.method == "POST":
        usuario.nome = request.POST.get("nome", "").strip()
        usuario.email = request.POST.get("email", "").strip()
        usuario.telefone = request.POST.get("telefone", "").strip()
        usuario.cidade = request.POST.get("cidade", "").strip()
        usuario.biografia = request.POST.get("biografia", "").strip()

        if request.FILES.get("foto_perfil"):
            usuario.foto_perfil = request.FILES["foto_perfil"]

        usuario.save()

        messages.success(request, "Alterações salvas com sucesso!")
        return redirect("perfil")

    return render(request, "perfil.html", {
        "usuario": usuario
    })


def conscientizacao(request):
    return render(request, "conscientizacao.html")


def mapa(request):
    produtos = Produto.objects.select_related("estabelecimento", "estabelecimento__usuario").filter(qtdEstoque__gt=0)
    return render(request, "mapa.html", {"produtos": produtos})


def detalhes_produto(request, produto_id=None):
    if produto_id is None:
        produto = Produto.objects.select_related(
            "estabelecimento", "estabelecimento__usuario", "categoria"
        ).filter(qtdEstoque__gt=0).first()
    else:
        produto = get_object_or_404(
            Produto.objects.select_related(
                "estabelecimento", "estabelecimento__usuario", "categoria"
            ),
            id=produto_id,
        )

    if produto is None:
        return redirect("index")

    return render(request, "detalhes_produto.html", {"produto": produto})


def cadastro_produto(request):
    usuario = exigir_login(request)
    if not isinstance(usuario, Usuario):
        return usuario

    try:
        estabelecimento = usuario.estabelecimento
    except Estabelecimento.DoesNotExist:
        messages.error(request, "Somente comerciantes podem cadastrar produtos.")
        return redirect("index")

    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(estabelecimento=estabelecimento)
            messages.success(request, "Produto cadastrado com sucesso.")
            return redirect("comercio")
    else:
        form = ProdutoForm()

    return render(request, "cadastro_produto.html", {"form": form})



def reservar_produto(request, produto_id):
    usuario = exigir_login(request)
    if not isinstance(usuario, Usuario):
        return usuario

    try:
        consumidor = usuario.consumidor
    except Consumidor.DoesNotExist:
        messages.error(request, "Somente consumidores podem reservar produtos.")
        return redirect("detalhes_produto", produto_id=produto_id)

    if request.method != "POST":
        return redirect("detalhes_produto", produto_id=produto_id)

    with transaction.atomic():
        produto = Produto.objects.select_for_update().get(id=produto_id)

        try:
            quantidade = int(request.POST.get("quantidade", "1"))
        except ValueError:
            quantidade = 1

        if quantidade < 1:
            quantidade = 1

        if produto.qtdEstoque < quantidade:
            messages.error(request, "Não há quantidade suficiente deste produto.")
            return redirect("detalhes_produto", produto_id=produto.id)

        Reserva.objects.create(
            consumidor=consumidor,
            produto=produto,
            quantidade=quantidade,
            status="Pendente",
        )

        produto.qtdEstoque -= quantidade
        produto.save(update_fields=["qtdEstoque"])

    messages.success(request, "Produto reservado com sucesso.")
    return redirect("minhas_reservas")


def minhas_reservas(request):
    usuario = exigir_login(request)
    if not isinstance(usuario, Usuario):
        return usuario

    try:
        consumidor = usuario.consumidor
    except Consumidor.DoesNotExist:
        messages.error(request, "Esta área é exclusiva para consumidores.")
        return redirect("comercio")

    reservas = Reserva.objects.select_related(
        "produto", "produto__estabelecimento", "produto__estabelecimento__usuario"
    ).filter(consumidor=consumidor).order_by("-dataReserva")

    return render(request, "minhas_reservas.html", {"reservas": reservas})


def comercio(request):
    usuario = exigir_login(request)
    if not isinstance(usuario, Usuario):
        return usuario

    try:
        estabelecimento = usuario.estabelecimento
    except Estabelecimento.DoesNotExist:
        messages.error(request, "Esta área é exclusiva para comerciantes.")
        return redirect("index")

    produtos = Produto.objects.filter(estabelecimento=estabelecimento).select_related("categoria").order_by("-id")

    reservas = Reserva.objects.filter(
        produto__estabelecimento=estabelecimento,
        status="Pendente"
    ).select_related("consumidor__usuario", "produto")

    return render(request, "comercio.html", {
        "estabelecimento": estabelecimento,
        "produtos": produtos,
        "reservas": reservas,
        "total_produtos": produtos.count(),
        "total_estoque": sum(p.qtdEstoque for p in produtos),
        "total_reservas": reservas.count(),
    })


def solicitacoes(request):
    return minhas_solicitacoes(request)


def minhas_solicitacoes(request):
    usuario = exigir_login(request)
    if not isinstance(usuario, Usuario):
        return usuario

    try:
        estabelecimento = usuario.estabelecimento
    except Estabelecimento.DoesNotExist:
        messages.error(request, "Área exclusiva para comerciantes.")
        return redirect("index")

    reservas = Reserva.objects.filter(
        produto__estabelecimento=estabelecimento
    ).select_related("produto", "consumidor__usuario").order_by("-dataReserva")

    return render(request, "solicitacoes.html", {"reservas": reservas})


def atualizar_reserva(request, reserva_id, status):
    usuario = exigir_login(request)
    if not isinstance(usuario, Usuario):
        return usuario

    try:
        estabelecimento = usuario.estabelecimento
    except Estabelecimento.DoesNotExist:
        return redirect("index")

    reserva = get_object_or_404(
        Reserva.objects.select_related("produto"),
        id=reserva_id,
        produto__estabelecimento=estabelecimento
    )

    if status == "confirmar":
        reserva.status = "Confirmada"
    elif status == "cancelar" and reserva.status != "Cancelada":
        reserva.status = "Cancelada"
        reserva.produto.qtdEstoque += reserva.quantidade
        reserva.produto.save(update_fields=["qtdEstoque"])
    else:
        return redirect("solicitacoes")

    reserva.save(update_fields=["status"])
    return redirect("solicitacoes")


def admin_dashboard(request):
    return render(request, "administrador.html")
