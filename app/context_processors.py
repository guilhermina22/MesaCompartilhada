from .models import NotificacaoPromocao, NotificacaoAvaliacao, Usuario


def usuario_contexto(request):
    usuario = None
    tipo_usuario = None
    usuario_id = request.session.get("usuario_id")
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            if hasattr(usuario, "estabelecimento"):
                tipo_usuario = "comerciante"
            elif hasattr(usuario, "consumidor"):
                tipo_usuario = "consumidor"
        except Usuario.DoesNotExist:
            pass

    notificacoes_nao_lidas = 0
    avaliacoes_nao_lidas = 0
    if usuario and tipo_usuario == "consumidor":
        notificacoes_nao_lidas = NotificacaoPromocao.objects.filter(consumidor=usuario.consumidor, lida=False).count()
    elif usuario and tipo_usuario == "comerciante":
        avaliacoes_nao_lidas = NotificacaoAvaliacao.objects.filter(estabelecimento=usuario.estabelecimento, lida=False).count()

    return {"usuario_logado": usuario, "tipo_usuario": tipo_usuario,
            "notificacoes_nao_lidas": notificacoes_nao_lidas,
            "avaliacoes_nao_lidas": avaliacoes_nao_lidas}
