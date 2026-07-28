from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def login_view(request):
    return render(request, "login.html")


def cadastro_consumidor(request):
    return render(request, "cadastro_consumidor.html")


def cadastro_comerciante(request):
    return render(request, "cadastro_comerciante.html")


def home(request):
    return render(request, "home.html")


def perfil(request):
    return render(request, "perfil.html")


def produtos(request):
    return render(request, "produtos.html")


def conscientizacao(request):
    return render(request, "conscientizacao.html")