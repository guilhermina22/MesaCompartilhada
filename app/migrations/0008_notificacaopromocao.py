from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("app", "0007_categorias_iniciais")]

    operations = [
        migrations.CreateModel(
            name="NotificacaoPromocao",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("lida", models.BooleanField(default=False, verbose_name="Lida")),
                ("criadaEm", models.DateTimeField(auto_now_add=True, verbose_name="Criada em")),
                ("consumidor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notificacoes_promocao", to="app.consumidor", verbose_name="Consumidor")),
                ("produto", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notificacoes_promocao", to="app.produto", verbose_name="Produto")),
            ],
            options={"verbose_name": "Notificação de promoção", "verbose_name_plural": "Notificações de promoções", "ordering": ["-criadaEm"]},
        ),
        migrations.AddConstraint(
            model_name="notificacaopromocao",
            constraint=models.UniqueConstraint(fields=("consumidor", "produto"), name="notificacao_unica_consumidor_produto"),
        ),
    ]
