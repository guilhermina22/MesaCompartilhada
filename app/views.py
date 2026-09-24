from django.contrib import messages
from django.db import transaction
from django.db.models import Avg, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    CadastroComercianteForm,
    CadastroConsumidorForm,
    EstabelecimentoForm,
    LoginForm,
    ProdutoForm,
    AvaliacaoProdutoForm,
    AvaliacaoEstabelecimentoForm,
)

from .models import (
    Categoria,
    Consumidor,
    Estabelecimento,
    NotificacaoPromocao,
    Produto,
    Reserva,
    Usuario,
    AvaliacaoProduto,
    AvaliacaoEstabelecimento,
    NotificacaoAvaliacao,
)


# =========================================================
# USUÁRIO / AUTENTICAÇÃO
# =========================================================

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


# =========================================================
# PÁGINA INICIAL
# =========================================================

def index(request):
    # Se ninguém estiver logado, mostra a landing page.
    if usuario_atual(request) is None:
        return render(request, "landing.html")

    busca = request.GET.get("busca", "").strip()
    categoria = request.GET.get("categoria", "").strip()
    preco = request.GET.get("preco", "").strip()

    produtos = Produto.objects.select_related(
        "estabelecimento",
        "estabelecimento__usuario",
        "categoria"
    ).filter(
        qtdEstoque__gt=0
    ).order_by("-id")

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca)
            | Q(estabelecimento__usuario__nome__icontains=busca)
        )

    if categoria:
        produtos = produtos.filter(
            categoria__nomeCategoria__iexact=categoria
        )

    if preco:
        try:
            produtos = produtos.filter(
                Q(precoPromocional__lte=float(preco))
                | Q(
                    precoPromocional__isnull=True,
                    precoOriginal__lte=float(preco)
                )
            )
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


# =========================================================
# LOGIN / LOGOUT
# =========================================================

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

    return render(request, "login.html", {
        "form": form
    })


def logout_view(request):
    request.session.flush()
    return redirect("index")


# =========================================================
# CADASTRO DE CONSUMIDOR
# =========================================================

def cadastro_consumidor(request):
    if request.method == "POST":
        form = CadastroConsumidorForm(request.POST)

        if form.is_valid():
            if Usuario.objects.filter(
                email=form.cleaned_data["email"]
            ).exists():

                form.add_error(
                    "email",
                    "Este e-mail já está cadastrado."
                )

            else:
                usuario = form.save(commit=False)
                usuario.senha = form.cleaned_data["senha"]
                usuario.save()

                Consumidor.objects.create(
                    usuario=usuario
                )

                request.session["usuario_id"] = usuario.id

                return redirect("index")

    else:
        form = CadastroConsumidorForm()

    return render(
        request,
        "cadastro_consumidor.html",
        {"form": form}
    )


# =========================================================
# CADASTRO DE COMERCIANTE
# =========================================================

def cadastro_comerciante(request):
    if request.method == "POST":

        form = CadastroComercianteForm(request.POST)
        estabelecimento_form = EstabelecimentoForm(request.POST)

        if form.is_valid() and estabelecimento_form.is_valid():

            if Usuario.objects.filter(
                email=form.cleaned_data["email"]
            ).exists():

                form.add_error(
                    "email",
                    "Este e-mail já está cadastrado."
                )

            else:
                usuario = form.save(commit=False)
                usuario.senha = form.cleaned_data["senha"]
                usuario.save()

                estabelecimento = estabelecimento_form.save(
                    commit=False
                )

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


# =========================================================
# PERFIL
# =========================================================

def perfil(request):
    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    if request.method == "POST":

        usuario.nome = request.POST.get(
            "nome", ""
        ).strip()

        usuario.email = request.POST.get(
            "email", ""
        ).strip()

        usuario.telefone = request.POST.get(
            "telefone", ""
        ).strip()

        usuario.cidade = request.POST.get(
            "cidade", ""
        ).strip()

        usuario.biografia = request.POST.get(
            "biografia", ""
        ).strip()

        if request.FILES.get("foto_perfil"):
            usuario.foto_perfil = request.FILES["foto_perfil"]

        usuario.save()

        messages.success(
            request,
            "Alterações salvas com sucesso!"
        )

        return redirect("perfil")

    return render(request, "perfil.html", {
        "usuario": usuario
    })


# =========================================================
# CONSCIENTIZAÇÃO
# =========================================================

def conscientizacao(request):
    return render(
        request,
        "conscientizacao.html"
    )


# =========================================================
# MAPA
# =========================================================

def mapa(request):
    produtos = Produto.objects.select_related(
        "estabelecimento",
        "estabelecimento__usuario"
    ).filter(
        qtdEstoque__gt=0
    )

    return render(
        request,
        "mapa.html",
        {"produtos": produtos}
    )


# =========================================================
# DETALHES DO PRODUTO
# =========================================================

def detalhes_produto(request, produto_id=None):

    if produto_id is None:

        produto = Produto.objects.select_related(
            "estabelecimento",
            "estabelecimento__usuario",
            "categoria"
        ).filter(
            qtdEstoque__gt=0
        ).first()

    else:

        produto = get_object_or_404(
            Produto.objects.select_related(
                "estabelecimento",
                "estabelecimento__usuario",
                "categoria"
            ),
            id=produto_id,
        )

    if produto is None:
        return redirect("index")

    avaliacoes = produto.avaliacoes.select_related(
        "consumidor__usuario"
    ).order_by(
        "-dataAvaliacao"
    )[:6]

    media_produto = produto.avaliacoes.aggregate(
        media=Avg("nota")
    )["media"]

    media_estabelecimento = (
        produto.estabelecimento.avaliacoes.aggregate(
            media=Avg("nota")
        )["media"]
    )

    return render(request, "detalhes_produto.html", {
        "produto": produto,
        "avaliacoes": avaliacoes,
        "media_produto": media_produto,
        "media_estabelecimento": media_estabelecimento,
    })


# =========================================================
# CADASTRO DE PRODUTO
# =========================================================

def cadastro_produto(request):
    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        estabelecimento = usuario.estabelecimento

    except Estabelecimento.DoesNotExist:

        messages.error(
            request,
            "Somente comerciantes podem cadastrar produtos."
        )

        return redirect("index")

    if request.method == "POST":

        form = ProdutoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            produto = form.save(
                estabelecimento=estabelecimento
            )

            # Cria uma notificação de promoção para
            # cada consumidor cadastrado.
            notificacoes = [
                NotificacaoPromocao(
                    consumidor=consumidor,
                    produto=produto
                )
                for consumidor in Consumidor.objects.all()
            ]

            NotificacaoPromocao.objects.bulk_create(
                notificacoes,
                ignore_conflicts=True
            )

            messages.success(
                request,
                "Produto cadastrado com sucesso. "
                "Os consumidores foram avisados da nova promoção."
            )

            return redirect("comercio")

    else:
        form = ProdutoForm()

    return render(request, "cadastro_produto.html", {
        "form": form
    })


# =========================================================
# RESERVAR PRODUTO
# =========================================================

def reservar_produto(request, produto_id):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        consumidor = usuario.consumidor

    except Consumidor.DoesNotExist:

        messages.error(
            request,
            "Somente consumidores podem reservar produtos."
        )

        return redirect(
            "detalhes_produto",
            produto_id=produto_id
        )

    if request.method != "POST":

        return redirect(
            "detalhes_produto",
            produto_id=produto_id
        )

    with transaction.atomic():

        produto = Produto.objects.select_for_update().get(
            id=produto_id
        )

        try:
            quantidade = int(
                request.POST.get("quantidade", "1")
            )

        except ValueError:
            quantidade = 1

        if quantidade < 1:
            quantidade = 1

        if produto.qtdEstoque < quantidade:

            messages.error(
                request,
                "Não há quantidade suficiente deste produto."
            )

            return redirect(
                "detalhes_produto",
                produto_id=produto.id
            )

        Reserva.objects.create(
            consumidor=consumidor,
            produto=produto,
            quantidade=quantidade,
            status="Pendente",
        )

        produto.qtdEstoque -= quantidade

        produto.save(
            update_fields=["qtdEstoque"]
        )

    messages.success(
        request,
        "Produto reservado com sucesso."
    )

    return redirect("minhas_reservas")


# =========================================================
# RESERVAS DO CONSUMIDOR
# =========================================================

def minhas_reservas(request):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        consumidor = usuario.consumidor

    except Consumidor.DoesNotExist:

        messages.error(
            request,
            "Esta área é exclusiva para consumidores."
        )

        return redirect("comercio")

    reservas = Reserva.objects.select_related(
        "produto",
        "produto__estabelecimento",
        "produto__estabelecimento__usuario"
    ).filter(
        consumidor=consumidor
    ).order_by(
        "-dataReserva"
    )

    return render(
        request,
        "minhas_reservas.html",
        {
            "reservas": reservas
        }
    )


# =========================================================
# PAINEL DO COMERCIANTE
# =========================================================

def comercio(request):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        estabelecimento = usuario.estabelecimento

    except Estabelecimento.DoesNotExist:

        messages.error(
            request,
            "Esta área é exclusiva para comerciantes."
        )

        return redirect("index")

    produtos = Produto.objects.filter(
        estabelecimento=estabelecimento
    ).select_related(
        "categoria"
    ).order_by(
        "-id"
    )

    reservas = Reserva.objects.filter(
        produto__estabelecimento=estabelecimento,
        status="Pendente"
    ).select_related(
        "consumidor__usuario",
        "produto"
    )

    avaliacoes_produtos = (
        AvaliacaoProduto.objects.filter(
            produto__estabelecimento=estabelecimento
        ).select_related(
            "produto",
            "consumidor__usuario"
        ).order_by(
            "-dataAvaliacao"
        )[:8]
    )

    avaliacoes_estabelecimento = (
        AvaliacaoEstabelecimento.objects.filter(
            estabelecimento=estabelecimento
        ).select_related(
            "consumidor__usuario"
        ).order_by(
            "-dataAvaliacao"
        )[:8]
    )

    return render(request, "comercio.html", {

        "estabelecimento": estabelecimento,

        "produtos": produtos,

        "reservas": reservas,

        "total_produtos": produtos.count(),

        "total_estoque": sum(
            p.qtdEstoque for p in produtos
        ),

        "total_reservas": reservas.count(),

        "avaliacoes_produtos":
            avaliacoes_produtos,

        "avaliacoes_estabelecimento":
            avaliacoes_estabelecimento,

        "media_produtos":
            AvaliacaoProduto.objects.filter(
                produto__estabelecimento=estabelecimento
            ).aggregate(
                media=Avg("nota")
            )["media"],

        "media_estabelecimento":
            AvaliacaoEstabelecimento.objects.filter(
                estabelecimento=estabelecimento
            ).aggregate(
                media=Avg("nota")
            )["media"],
    })


# =========================================================
# SOLICITAÇÕES
# =========================================================

def solicitacoes(request):
    return minhas_solicitacoes(request)


def minhas_solicitacoes(request):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        estabelecimento = usuario.estabelecimento

    except Estabelecimento.DoesNotExist:

        messages.error(
            request,
            "Área exclusiva para comerciantes."
        )

        return redirect("index")

    reservas = Reserva.objects.filter(
        produto__estabelecimento=estabelecimento
    ).select_related(
        "produto",
        "consumidor__usuario"
    ).order_by(
        "-dataReserva"
    )

    return render(
        request,
        "solicitacoes.html",
        {"reservas": reservas}
    )


# =========================================================
# ATUALIZAR RESERVA
# =========================================================

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

    elif (
        status == "cancelar"
        and reserva.status != "Cancelada"
    ):

        reserva.status = "Cancelada"

        reserva.produto.qtdEstoque += reserva.quantidade

        reserva.produto.save(
            update_fields=["qtdEstoque"]
        )

    else:
        return redirect("solicitacoes")

    reserva.save(
        update_fields=["status"]
    )

    return redirect("solicitacoes")


# =========================================================
# ADMIN
# =========================================================

def admin_dashboard(request):
    return render(
        request,
        "administrador.html"
    )


# =========================================================
# PROMOÇÕES
# =========================================================

def promocoes(request):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        consumidor = usuario.consumidor

    except Consumidor.DoesNotExist:

        messages.error(
            request,
            "A página de promoções é exclusiva para consumidores."
        )

        return redirect("comercio")

    categoria = request.GET.get(
        "categoria", ""
    ).strip()

    busca = request.GET.get(
        "busca", ""
    ).strip()

    produtos = Produto.objects.select_related(
        "estabelecimento",
        "estabelecimento__usuario",
        "categoria"
    ).filter(
        qtdEstoque__gt=0
    ).order_by(
        "-id"
    )

    if categoria:

        produtos = produtos.filter(
            categoria__nomeCategoria__iexact=categoria
        )

    if busca:

        produtos = produtos.filter(
            Q(nome__icontains=busca)
            | Q(
                estabelecimento__usuario__nome__icontains=busca
            )
        )

    notificacoes = (
        NotificacaoPromocao.objects.select_related(
            "produto",
            "produto__estabelecimento",
            "produto__estabelecimento__usuario"
        ).filter(
            consumidor=consumidor
        )[:12]
    )

    return render(request, "promocoes.html", {

        "produtos": produtos,

        "categorias":
            Categoria.objects.all().order_by(
                "nomeCategoria"
            ),

        "categoria": categoria,

        "busca": busca,

        "notificacoes": notificacoes,
    })


# =========================================================
# NOTIFICAÇÕES DE PROMOÇÕES
# =========================================================

def marcar_notificacao_lida(
    request,
    notificacao_id
):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return JsonResponse(
            {"ok": False},
            status=401
        )

    if request.method != "POST":

        return JsonResponse(
            {"ok": False},
            status=405
        )

    try:
        consumidor = usuario.consumidor

    except Consumidor.DoesNotExist:

        return JsonResponse(
            {"ok": False},
            status=403
        )

    notificacao = get_object_or_404(
        NotificacaoPromocao,
        id=notificacao_id,
        consumidor=consumidor
    )

    notificacao.lida = True

    notificacao.save(
        update_fields=["lida"]
    )

    restantes = NotificacaoPromocao.objects.filter(
        consumidor=consumidor,
        lida=False
    ).count()

    return JsonResponse({
        "ok": True,
        "nao_lidas": restantes
    })


def marcar_todas_notificacoes_lidas(request):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):

        return JsonResponse(
            {"ok": False},
            status=401
        )

    if request.method != "POST":

        return JsonResponse(
            {"ok": False},
            status=405
        )

    try:
        consumidor = usuario.consumidor

    except Consumidor.DoesNotExist:

        return JsonResponse(
            {"ok": False},
            status=403
        )

    NotificacaoPromocao.objects.filter(
        consumidor=consumidor,
        lida=False
    ).update(
        lida=True
    )

    return JsonResponse({
        "ok": True,
        "nao_lidas": 0
    })


# =========================================================
# EXCLUIR PRODUTO
# =========================================================

def excluir_produto(request, produto_id):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        estabelecimento = usuario.estabelecimento

    except Estabelecimento.DoesNotExist:

        messages.error(
            request,
            "Somente comerciantes podem excluir produtos."
        )

        return redirect("index")

    produto = get_object_or_404(
        Produto,
        id=produto_id,
        estabelecimento=estabelecimento
    )

    if request.method == "POST":

        nome = produto.nome

        produto.delete()

        messages.success(
            request,
            f'Produto "{nome}" excluído. '
            "Ele não está mais visível para os consumidores."
        )

    return redirect("comercio")


# =========================================================
# PÁGINA DE AVALIAÇÕES DO CONSUMIDOR
# =========================================================

def avaliacoes(request):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        consumidor = usuario.consumidor

    except Consumidor.DoesNotExist:
        return redirect("feedbacks_comercio")

    # -----------------------------------------------------
    # IMPORTANTE:
    # Só buscamos produtos que ESTE consumidor reservou.
    #
    # Produtos antigos continuam funcionando normalmente.
    # Não importa quando o produto foi cadastrado.
    #
    # A única exigência é existir uma reserva não cancelada.
    # -----------------------------------------------------

    produtos_reservados_ids = Reserva.objects.filter(
        consumidor=consumidor
    ).exclude(
        status="Cancelada"
    ).values_list(
        "produto_id",
        flat=True
    ).distinct()

    produtos = Produto.objects.select_related(
        "estabelecimento__usuario"
    ).filter(
        id__in=produtos_reservados_ids
    ).order_by(
        "nome"
    )

    # -----------------------------------------------------
    # ESTABELECIMENTOS
    #
    # Continua exatamente como anteriormente:
    # o consumidor pode avaliar os estabelecimentos.
    # -----------------------------------------------------

    estabelecimentos = (
        Estabelecimento.objects.select_related(
            "usuario"
        ).order_by(
            "usuario__nome"
        )
    )

    # Avaliações de produtos já realizadas
    minhas_produto = (
        AvaliacaoProduto.objects.filter(
            consumidor=consumidor
        ).select_related(
            "produto"
        ).order_by(
            "-dataAvaliacao"
        )
    )

    # Avaliações de estabelecimentos já realizadas
    minhas_estabelecimento = (
        AvaliacaoEstabelecimento.objects.filter(
            consumidor=consumidor
        ).select_related(
            "estabelecimento__usuario"
        ).order_by(
            "-dataAvaliacao"
        )
    )

    return render(request, "avaliacoes.html", {

        "produtos": produtos,

        "estabelecimentos":
            estabelecimentos,

        "minhas_produto":
            minhas_produto,

        "minhas_estabelecimento":
            minhas_estabelecimento,

        "form_produto":
            AvaliacaoProdutoForm(),

        "form_estabelecimento":
            AvaliacaoEstabelecimentoForm(),
    })


# =========================================================
# AVALIAR PRODUTO
# =========================================================

def avaliar_produto(request, produto_id):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        consumidor = usuario.consumidor

    except Consumidor.DoesNotExist:

        messages.error(
            request,
            "Somente consumidores podem avaliar produtos."
        )

        return redirect("comercio")

    produto = get_object_or_404(
        Produto,
        id=produto_id
    )

    # =====================================================
    # VERIFICAÇÃO DA RESERVA
    #
    # O consumidor precisa ter reservado este produto.
    #
    # Reservas canceladas NÃO permitem avaliação.
    #
    # Isso protege também o backend. Portanto, mesmo que
    # alguém tente acessar manualmente a URL, não conseguirá
    # avaliar um produto que nunca reservou.
    # =====================================================

    possui_reserva = Reserva.objects.filter(
        consumidor=consumidor,
        produto=produto
    ).exclude(
        status="Cancelada"
    ).exists()

    if not possui_reserva:

        messages.error(
            request,
            "Você só pode avaliar produtos que já reservou."
        )

        return redirect("avaliacoes")

    # A avaliação só pode ser enviada por POST.
    if request.method != "POST":
        return redirect("avaliacoes")

    form = AvaliacaoProdutoForm(
        request.POST
    )

    if form.is_valid():

        # Procura uma avaliação anterior deste consumidor
        # para este mesmo produto.
        avaliacao = (
            AvaliacaoProduto.objects.filter(
                consumidor=consumidor,
                produto=produto
            ).first()
        )

        # Se nunca avaliou, cria uma nova.
        if avaliacao is None:

            avaliacao = form.save(
                commit=False
            )

            avaliacao.consumidor = consumidor
            avaliacao.produto = produto

        # Se já avaliou, apenas atualiza.
        else:

            avaliacao.nota = (
                form.cleaned_data["nota"]
            )

            avaliacao.comentario = (
                form.cleaned_data["comentario"]
            )

        avaliacao.dataAvaliacao = timezone.now()

        avaliacao.save()

        # -------------------------------------------------
        # NOTIFICAÇÃO DO COMERCIANTE
        # -------------------------------------------------

        # Se havia uma notificação não lida dessa avaliação,
        # removemos antes de criar a nova.
        NotificacaoAvaliacao.objects.filter(
            avaliacao_produto=avaliacao,
            lida=False
        ).delete()

        # Cria a notificação para o estabelecimento.
        NotificacaoAvaliacao.objects.create(
            estabelecimento=produto.estabelecimento,
            avaliacao_produto=avaliacao
        )

        messages.success(
            request,
            "Avaliação do produto salva com sucesso."
        )

    else:

        messages.error(
            request,
            "Não foi possível salvar a avaliação. "
            "Verifique a nota e o comentário."
        )

    return redirect("avaliacoes")


# =========================================================
# AVALIAR ESTABELECIMENTO
# =========================================================

def avaliar_estabelecimento(
    request,
    estabelecimento_id
):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        consumidor = usuario.consumidor

    except Consumidor.DoesNotExist:

        messages.error(
            request,
            "Somente consumidores podem avaliar estabelecimentos."
        )

        return redirect("comercio")

    estabelecimento = get_object_or_404(
        Estabelecimento,
        id=estabelecimento_id
    )

    if request.method != "POST":
        return redirect("avaliacoes")

    form = AvaliacaoEstabelecimentoForm(
        request.POST
    )

    if form.is_valid():

        avaliacao = (
            AvaliacaoEstabelecimento.objects.filter(
                consumidor=consumidor,
                estabelecimento=estabelecimento
            ).first()
        )

        if avaliacao is None:

            avaliacao = form.save(
                commit=False
            )

            avaliacao.consumidor = consumidor
            avaliacao.estabelecimento = estabelecimento

        else:

            avaliacao.nota = (
                form.cleaned_data["nota"]
            )

            avaliacao.comentario = (
                form.cleaned_data["comentario"]
            )

        avaliacao.dataAvaliacao = timezone.now()

        avaliacao.save()

        # Remove notificação anterior ainda não lida.
        NotificacaoAvaliacao.objects.filter(
            avaliacao_estabelecimento=avaliacao,
            lida=False
        ).delete()

        # Notifica o estabelecimento.
        NotificacaoAvaliacao.objects.create(
            estabelecimento=estabelecimento,
            avaliacao_estabelecimento=avaliacao
        )

        messages.success(
            request,
            "Avaliação do estabelecimento salva com sucesso."
        )

    else:

        messages.error(
            request,
            "Não foi possível salvar a avaliação."
        )

    return redirect("avaliacoes")


# =========================================================
# FEEDBACKS DO COMERCIANTE
# =========================================================

def feedbacks_comercio(request):

    usuario = exigir_login(request)

    if not isinstance(usuario, Usuario):
        return usuario

    try:
        estabelecimento = usuario.estabelecimento

    except Estabelecimento.DoesNotExist:
        return redirect("avaliacoes")

    # Últimas notificações recebidas.
    notificacoes_avaliacao = (
        NotificacaoAvaliacao.objects.filter(
            estabelecimento=estabelecimento
        ).select_related(
            "avaliacao_produto__produto",
            "avaliacao_estabelecimento"
        ).order_by(
            "-criadaEm"
        )[:20]
    )

    # Ao abrir a página de feedbacks,
    # as notificações são marcadas como lidas.
    NotificacaoAvaliacao.objects.filter(
        estabelecimento=estabelecimento,
        lida=False
    ).update(
        lida=True
    )

    # Feedbacks dos produtos.
    produto_feedbacks = (
        AvaliacaoProduto.objects.filter(
            produto__estabelecimento=estabelecimento
        ).select_related(
            "produto",
            "consumidor__usuario"
        ).order_by(
            "-dataAvaliacao"
        )
    )

    # Feedbacks do estabelecimento.
    estabelecimento_feedbacks = (
        AvaliacaoEstabelecimento.objects.filter(
            estabelecimento=estabelecimento
        ).select_related(
            "consumidor__usuario"
        ).order_by(
            "-dataAvaliacao"
        )
    )

    return render(
        request,
        "feedbacks_comercio.html",
        {
            "produto_feedbacks":
                produto_feedbacks,

            "estabelecimento_feedbacks":
                estabelecimento_feedbacks,

            "media_produtos":
                produto_feedbacks.aggregate(
                    media=Avg("nota")
                )["media"],

            "media_estabelecimento":
                estabelecimento_feedbacks.aggregate(
                    media=Avg("nota")
                )["media"],

            "notificacoes_avaliacao":
                notificacoes_avaliacao,
        }
    )