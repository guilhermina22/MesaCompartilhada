from django import forms
from .models import Usuario, Estabelecimento, Produto, Categoria


class CadastroConsumidorForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(), label="Confirmar senha")

    class Meta:
        model = Usuario
        fields = ["nome", "email", "senha", "telefone"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("senha") != cleaned.get("confirmar_senha"):
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned


class CadastroComercianteForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(), label="Confirmar senha")

    class Meta:
        model = Usuario
        fields = ["nome", "email", "senha", "telefone"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("senha") != cleaned.get("confirmar_senha"):
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned


class EstabelecimentoForm(forms.ModelForm):
    class Meta:
        model = Estabelecimento
        fields = ["descricao", "endereco"]


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail")
    senha = forms.CharField(widget=forms.PasswordInput(), label="Senha")


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome",
            "descricao",
            "precoOriginal",
            "quantidade",
            "dataValidade",
            "imagem",
            "categoria",
        ]
        labels = {
            "nome": "Nome do produto",
            "descricao": "Descrição",
            "precoOriginal": "Preço de venda",
            "quantidade": "Quantidade disponível",
            "dataValidade": "Data de validade",
            "imagem": "Imagem do produto",
            "categoria": "Categoria",
        }
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
            "dataValidade": forms.DateInput(attrs={"type": "date"}),
            "imagem": forms.ClearableFileInput(),
            "precoOriginal": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "quantidade": forms.NumberInput(attrs={"min": "1"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].queryset = Categoria.objects.all().order_by("nomeCategoria")
        self.fields["categoria"].empty_label = "Selecione uma categoria"

    def save(self, commit=True, estabelecimento=None):
        produto = super().save(commit=False)
        if estabelecimento is not None:
            produto.estabelecimento = estabelecimento
        produto.status = "Disponível"
        produto.qtdEstoque = produto.quantidade
        if commit:
            produto.save()
        return produto
