from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Produto, Usuario


def index(request):
    # Pega os filtros enviados pela página
    busca = request.GET.get("busca", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    preco = request.GET.get("preco", "").strip()

    # Busca todos os produtos
    produtos = Produto.objects.select_related(
        "estabelecimento",
        "estabelecimento__usuario",
        "categoria"
    ).all()

    # Filtro de busca
    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) |
            Q(estabelecimento__usuario__nome__icontains=busca)
        )

    # Filtro de categoria
    if categoria:
        produtos = produtos.filter(
            categoria__nomeCategoria__iexact=categoria
        )

    # Filtro de preço
    if preco:
        try:
            produtos = produtos.filter(
                precoOriginal__lte=float(preco)
            )
        except (ValueError, TypeError):
            pass

    # Envia os produtos para o HTML
    context = {
        "produtos": produtos,
        "busca": busca,
        "categoria": categoria,
        "preco": preco,
    }

    return render(request, "index.html", context)


def login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        senha = request.POST.get("senha")

        try:
            usuario = Usuario.objects.get(
                email=email,
                senha=senha
            )

            request.session["usuario_id"] = usuario.id

            return redirect("perfil")

        except Usuario.DoesNotExist:

            return render(
                request,
                "login.html",
                {
                    "erro": "E-mail ou senha incorretos."
                }
            )

    return render(request, "login.html")


def cadastro_consumidor(request):
    return render(request, "cadastro_consumidor.html")


def cadastro_comerciante(request):
    return render(request, "cadastro_comerciante.html")


def perfil(request):

    usuario_id = request.session.get("usuario_id")

    if not usuario_id:
        return redirect("login")

    try:
        usuario = Usuario.objects.get(id=usuario_id)

    except Usuario.DoesNotExist:
        request.session.flush()
        return redirect("login")

    return render(
        request,
        "perfil.html",
        {
            "usuario": usuario
        }
    )


def conscientizacao(request):
    return render(request, "conscientizacao.html")


def mapa(request):
    return render(request, "mapa.html")


def detalhes_doacao(request):
    return render(request, "detalhes_doacao.html")


def cadastro_doacao(request):
    return render(request, "cadastro_doacao.html")


def explorar_doacoes(request):
    return render(request, "explorar_doacoes.html")


def comercio(request):
    return render(request, "comercio.html")


def solicitacoes(request):
    return render(request, "solicitacoes.html")


def admin_dashboard(request):
    return render(request, "administrador.html")