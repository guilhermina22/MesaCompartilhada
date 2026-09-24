from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0008_notificacaopromocao"),
    ]

    operations = [
        migrations.AddField(
            model_name="produto",
            name="precoPromocional",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name="Preço promocional"),
        ),
        migrations.AlterField(
            model_name="produto",
            name="precoOriginal",
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Preço original"),
        ),
    ]
