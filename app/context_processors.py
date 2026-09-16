from .models import Usuario


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

    return {
        "usuario_logado": usuario,
        "tipo_usuario": tipo_usuario,
    }
