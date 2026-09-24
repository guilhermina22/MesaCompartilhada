from django import forms
from .models import (
    Usuario, Estabelecimento, Produto, Categoria,
    AvaliacaoProduto, AvaliacaoEstabelecimento,
)


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
            "precoPromocional",
            "quantidade",
            "dataValidade",
            "imagem",
            "categoria",
        ]
        labels = {
            "nome": "Nome do produto",
            "descricao": "Descrição",
            "precoOriginal": "Preço original (de)",
            "precoPromocional": "Preço promocional (por)",
            "quantidade": "Quantidade disponível",
            "dataValidade": "Data de validade",
            "imagem": "Imagem do produto",
            "categoria": "Categoria",
        }
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
            "dataValidade": forms.DateInput(attrs={"type": "date"}),
            "imagem": forms.ClearableFileInput(),
            "precoOriginal": forms.NumberInput(attrs={"step": "0.01", "min": "0.01", "placeholder": "Ex.: 12,90"}),
            "precoPromocional": forms.NumberInput(attrs={"step": "0.01", "min": "0.01", "placeholder": "Ex.: 7,90"}),
            "quantidade": forms.NumberInput(attrs={"min": "1"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].queryset = Categoria.objects.all().order_by("nomeCategoria")
        self.fields["categoria"].empty_label = "Selecione uma categoria"


    def clean(self):
        cleaned = super().clean()
        original = cleaned.get("precoOriginal")
        promocional = cleaned.get("precoPromocional")
        if promocional is None:
            self.add_error("precoPromocional", "Informe o preço promocional.")
        elif original is not None and promocional >= original:
            self.add_error("precoPromocional", "O preço promocional deve ser menor que o preço original.")
        return cleaned

    def save(self, commit=True, estabelecimento=None):
        produto = super().save(commit=False)
        if estabelecimento is not None:
            produto.estabelecimento = estabelecimento
        produto.status = "Disponível"
        produto.qtdEstoque = produto.quantidade
        if commit:
            produto.save()
        return produto


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "nome",
            "email",
            "telefone",
            "cidade",
            "biografia",
            "foto_perfil",
        ]


class AvaliacaoProdutoForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoProduto
        fields = ["nota", "comentario"]
        labels = {"nota": "Nota do produto", "comentario": "Comentário sobre o produto"}
        widgets = {
            "nota": forms.Select(choices=[(5, "5 - Excelente"), (4, "4 - Muito bom"), (3, "3 - Bom"), (2, "2 - Regular"), (1, "1 - Ruim")]),
            "comentario": forms.Textarea(attrs={"rows": 4, "placeholder": "Conte como foi sua experiência com este produto..."}),
        }

    def clean_nota(self):
        nota = self.cleaned_data["nota"]
        if nota < 1 or nota > 5:
            raise forms.ValidationError("A nota deve estar entre 1 e 5.")
        return nota


class AvaliacaoEstabelecimentoForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoEstabelecimento
        fields = ["nota", "comentario"]
        labels = {"nota": "Nota do estabelecimento", "comentario": "Comentário sobre o estabelecimento"}
        widgets = {
            "nota": forms.Select(choices=[(5, "5 - Excelente"), (4, "4 - Muito bom"), (3, "3 - Bom"), (2, "2 - Regular"), (1, "1 - Ruim")]),
            "comentario": forms.Textarea(attrs={"rows": 4, "placeholder": "Conte como foi sua experiência com este estabelecimento..."}),
        }

    def clean_nota(self):
        nota = self.cleaned_data["nota"]
        if nota < 1 or nota > 5:
            raise forms.ValidationError("A nota deve estar entre 1 e 5.")
        return nota
