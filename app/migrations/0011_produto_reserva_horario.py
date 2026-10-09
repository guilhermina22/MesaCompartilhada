from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("app", "0010_merge_20260924_0902")]
    operations = [
        migrations.AddField(model_name="produto", name="permite_reserva", field=models.BooleanField(default=True, verbose_name="Permite reserva pelo site")),
        migrations.AddField(model_name="produto", name="cadastrado_em", field=models.DateTimeField(auto_now_add=True, null=True, verbose_name="Data e hora do cadastro")),
    ]
