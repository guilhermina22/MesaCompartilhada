# from django.shortcuts import render


# def index(request):
#     return render(request, 'index.html')


# def login(request):
#     return render(request, 'login.html')


# def cadastro_consumidor(request):
#     return render(request, 'cadastro_consumidor.html')


# def cadastro_comerciante(request):
#     return render(request, 'cadastro_comerciante.html')


# # def home(request):
# #     return render(request, 'home.html')


# def perfil(request):
#     return render(request, 'perfil.html')


# # def produtos(request):
# #     return render(request, 'produtos.html')


# def conscientizacao(request):
#     return render(request, 'conscientizacao.html')



# # NOVAS TELAS


# def mapa(request):
#     return render(request, 'mapa.html')


# def detalhes_doacao(request):
#     return render(request, 'detalhes_doacao.html')


# def cadastro_doacao(request):
#     return render(request, 'cadastro_doacao.html')

# def explorar_doacoes(request):
#     return render(request, 'explorar_doacoes.html')


# def comercio(request):
#     return render(request, 'comercio.html')


# def solicitacoes(request):
#     return render(request, 'solicitacoes.html')


# def admin_dashboard(request):
#     return render(request, 'administrador.html')


from django.shortcuts import render
from django.db.models import Q
from .models import Produto

def index(request):

    busca = request.GET.get('busca', '')
    categoria = request.GET.get('categoria', '')
    preco = request.GET.get('preco', '')

    produtos = Produto.objects.all()

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) |
            Q(estabelecimento__usuario__nome__icontains=busca)
        )

    if categoria:
        produtos = produtos.filter(
            categoria__nomeCategoria=categoria
        )
        
    if preco:
        produtos = produtos.filter(precoOriginal__lte=preco)

    context = {
        'produtos': produtos,
        'busca': busca,
        'categoria': categoria,
        'preco': preco,
    }

    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html')


def cadastro_consumidor(request):
    return render(request, 'cadastro_consumidor.html')


def cadastro_comerciante(request):
    return render(request, 'cadastro_comerciante.html')


def perfil(request):
    return render(request, 'perfil.html')


def conscientizacao(request):
    return render(request, 'conscientizacao.html')


def mapa(request):
    return render(request, 'mapa.html')


def detalhes_doacao(request):
    return render(request, 'detalhes_doacao.html')


def cadastro_doacao(request):
    return render(request, 'cadastro_doacao.html')


def explorar_doacoes(request):
    return render(request, 'explorar_doacoes.html')


def comercio(request):
    return render(request, 'comercio.html')


def solicitacoes(request):
    return render(request, 'solicitacoes.html')


def admin_dashboard(request):
    return render(request, 'administrador.html')