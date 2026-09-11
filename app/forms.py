from django import forms
from .models import Usuario, Estabelecimento


class CadastroConsumidorForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(),
        label="Senha"
    )

    class Meta:
        model = Usuario
        fields = [
            "nome",
            "email",
            "senha",
            "telefone",
        ]


class CadastroComercianteForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(),
        label="Senha"
    )

    class Meta:
        model = Usuario
        fields = [
            "nome",
            "email",
            "senha",
            "telefone",
        ]


class EstabelecimentoForm(forms.ModelForm):
    descricao = forms.CharField(
        label="Descrição"
    )

    endereco = forms.CharField(
        label="Endereço"
    )

    class Meta:
        model = Estabelecimento
        fields = [
            "descricao",
            "endereco",
        ]


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="E-mail"
    )

    senha = forms.CharField(
        widget=forms.PasswordInput(),
        label="Senha"
    )