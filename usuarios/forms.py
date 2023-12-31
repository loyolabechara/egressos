from django import forms
from .models import *
from .functions import validate_CPF


class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class CadastrarForm(ModelForm):

    nome = forms.CharField(label = 'Nome:')
    email = forms.CharField(label = 'E-Mail:')
    cpf = forms.CharField(label='CPF', max_length=14, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icpf)"}))
    celular = forms.CharField(label= "Celular", max_length=15, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icelular)", 'onload' : 'mascara(this,icelular)'}))
    cep = forms.CharField(label = 'CEP', max_length= 10, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icep)", 'onload' : 'mascara(this,icep)'}))
#    dtNascimento = forms.DateField(label='Dt. Nascimento:', required=True, widget=DateInput(attrs={'type': 'date'}))

    dtNascimento = forms.DateField(label='Data de Nascimento:', widget = forms.DateInput(attrs={'class': 'form-control', 'placeholder':'DD/MM/AAAA', 'onkeydown':'mascara(this,data)', 'onload' : 'mascara(this,data)', 'maxlength':'10'}))

    senha = forms.CharField(label = 'Senha:', widget=forms.PasswordInput)
    senha_confirma = forms.CharField(label = 'Confirmação de senha:', widget=forms.PasswordInput)
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), widget = forms.Select(attrs={'class': "selEstado"}))
#    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), widget = forms.Select(attrs={'class': "selCidade"}))
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    field_order = ['nome', 'email', 'cpf', 'sexo', 'dtNascimento', 'celular', 'rua', 'numero', 'complemento', 'estado', 'cidade', 'cep', 'senha', 'senha_confirma']

    def clean_dtNascimento(self):
        from datetime import date

        today = date.today()

        dtNascimentoAux = self.cleaned_data["dtNascimento"]

        idade = today.year - dtNascimentoAux.year - ((today.month, today.day) < (dtNascimentoAux.month, dtNascimentoAux.day))

        if idade < 18:
            raise ValidationError('Permitido apenas para pessoas maiores de 18 anos.')

        return self.cleaned_data["dtNascimento"]
    def clean_senha_confirma(self):
        if self.cleaned_data["senha"] != self.cleaned_data["senha_confirma"]:
            raise ValidationError('Senha não confirmada corretamente.')
        
        if len(self.cleaned_data["senha_confirma"]) < 6 or len(self.cleaned_data["senha_confirma"]) > 12:
            raise ValidationError('Senha precisa ter no mínimo 6 e no máximo 12 caracteres, com pelo menos uma letra e um número.')

        # verifica se tem pelo menos 1 letra
        encontrou = False
        for char in self.cleaned_data["senha_confirma"]:
            if char.isalpha():
                encontrou = True
                break
        if not encontrou:
            raise ValidationError('Senha precisa ter pelo menos 1 letra.')
       # verifica se tem pelo menos 1 letra
        encontrou = False
        for char in self.cleaned_data["senha_confirma"]:
            if char.isdigit():
                encontrou = True
                break
        if not encontrou:
            raise ValidationError('Senha precisa ter pelo menos 1 numero.')

        return self.cleaned_data["senha_confirma"]
    def clean_cpf(self):
        cpf = validate_CPF(self.cleaned_data["cpf"])
        cpf = cpf.replace('.','')
        cpf = cpf.replace('-','')
        return cpf
    def clean_celular(self):
        telefone = self.cleaned_data["celular"]
        telefone = telefone.replace("(",'')
        telefone = telefone.replace(")",'')
        telefone = telefone.replace("-",'')
        telefone = telefone.replace(" ",'')
        if len(telefone) == 10:
            if telefone[2:3] != '2':
                raise ValidationError('Insira um número válido.')
        else:
            if len(telefone) != 11:
                raise ValidationError('Insira um número válido.')
        return telefone
    def clean_cep(self):
        cep = self.cleaned_data["cep"]
        cep = cep.replace(".",'')
        cep = cep.replace("-",'')
        if len(cep) != 8:
            raise ValidationError('Insira um CEP válido.')
        return cep

    class Meta:
        model = Usuario
        exclude = ['user', 'ativo', 'dt_inclusao']
