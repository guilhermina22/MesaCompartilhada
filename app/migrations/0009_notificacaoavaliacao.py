from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [('app', '0008_notificacaopromocao')]
    operations = [
        migrations.CreateModel(
            name='NotificacaoAvaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lida', models.BooleanField(default=False, verbose_name='Lida')),
                ('criadaEm', models.DateTimeField(auto_now_add=True, verbose_name='Criada em')),
                ('avaliacao_estabelecimento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes_comerciante', to='app.avaliacaoestabelecimento', verbose_name='Avaliação do estabelecimento')),
                ('avaliacao_produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes_comerciante', to='app.avaliacaoproduto', verbose_name='Avaliação de produto')),
                ('estabelecimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificacoes_avaliacao', to='app.estabelecimento', verbose_name='Estabelecimento')),
            ],
            options={'verbose_name':'Notificação de avaliação','verbose_name_plural':'Notificações de avaliações','ordering':['-criadaEm']},
        ),
    ]
