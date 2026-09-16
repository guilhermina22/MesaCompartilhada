from django.db import migrations


def criar_categorias(apps, schema_editor):
    Categoria = apps.get_model("app", "Categoria")
    nomes = [
        "Padaria",
        "Frutas",
        "Verduras",
        "Laticínios",
        "Confeitaria",
    ]
    for nome in nomes:
        Categoria.objects.get_or_create(nomeCategoria=nome)


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_reserva"),
    ]

    operations = [
        migrations.RunPython(criar_categorias, migrations.RunPython.noop),
    ]
