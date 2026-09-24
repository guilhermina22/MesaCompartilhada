from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_usuario_biografia_usuario_cidade_usuario_foto_perfil"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reserva",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantidade",
                    models.PositiveIntegerField(
                        default=1,
                        verbose_name="Quantidade",
                    ),
                ),
                (
                    "dataReserva",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Data da reserva",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        default="Pendente",
                        max_length=30,
                        verbose_name="Status",
                    ),
                ),
                (
                    "consumidor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservas",
                        to="app.consumidor",
                        verbose_name="Consumidor",
                    ),
                ),
                (
                    "produto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservas",
                        to="app.produto",
                        verbose_name="Produto",
                    ),
                ),
            ],
            options={
                "verbose_name": "Reserva",
                "verbose_name_plural": "Reservas",
            },
        ),
    ]
