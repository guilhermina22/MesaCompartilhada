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

    descricao = forms.CharField(
        label="Descrição"
    )

    endereco = forms.CharField(
        label="Endereço"
    )

    class Meta:
        model = Usuario
        fields = [
            "nome",
            "email",
            "senha",
            "telefone",
        ]


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="E-mail"
    )

    senha = forms.CharField(
        widget=forms.PasswordInput(),
        label="Senha"
    )