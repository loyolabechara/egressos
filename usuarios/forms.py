from django import forms
from django.forms import ModelForm, ValidationError
from .models import *
from .functions_cpf_cnpj import validate_CPF


class LoginForm(forms.Form):
    email = forms.CharField(label='E-Mail:')
    senha = forms.CharField(max_length=20, widget=forms.PasswordInput)
    next = forms.CharField(widget = forms.HiddenInput(), required = False)


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
    dtNascimento = forms.DateField(label='Data Nascimento', widget=DateInput(attrs={'type': 'date'}))

#    dtNascimento = forms.DateField(label='Data de Nascimento:', widget = forms.DateInput(attrs={'class': 'form-control', 'placeholder':'DD/MM/AAAA', 'onkeydown':'mascara(this,data)', 'onload' : 'mascara(this,data)', 'maxlength':'10'}))

    senha = forms.CharField(label = 'Senha:', widget=forms.PasswordInput)
    senha_confirma = forms.CharField(label = 'Confirmação de senha:', widget=forms.PasswordInput)
#    pais = forms.ModelChoiceField(queryset=Pais.objects.all(), widget = forms.Select(attrs={'class': "selPais"}))
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), required=False, widget = forms.Select(attrs={'class': "selEstado"}))


#    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), widget = forms.Select(attrs={'class': "selCidade"}))
#    captcha = ReCaptchaField(widget=ReCaptchaV3)

    field_order = ['nome', 'email', 'cpf', 'sexo', 'dtNascimento', 'celular', 'rua', 'numero', 'complemento', 'pais', 'estado', 'cidade', 'estado_exterior', 'cidade_exterior', 'cep', 'senha', 'senha_confirma']

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





class CadastroAlteraForm(ModelForm):

    nome = forms.CharField(label = 'Nome:')
    cpf = forms.CharField(label='CPF', max_length=14, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icpf)"}))
    celular = forms.CharField(label= "Celular", max_length=15, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icelular)", 'onload' : 'mascara(this,icelular)'}))
    cep = forms.CharField(label = 'CEP', max_length= 10, widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icep)", 'onload' : 'mascara(this,icep)'}))
    dtNascimento = forms.DateField(label='Dt. Nascimento:', required=True, widget=DateInput(attrs={'type': 'date'}))
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), widget = forms.Select(attrs={'class': "selEstado"}))
#    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), widget = forms.Select(attrs={'class': "selCidade"}))

    field_order = ['nome', 'cpf', 'sexo', 'dtNascimento', 'celular', 'rua', 'numero', 'complemento', 'pais', 'estado', 'cidade', 'estado_exterior', 'cidade_exterior', 'cep']

    def clean_dtNascimento(self):
        from datetime import date

        today = date.today()

        dtNascimentoAux = self.cleaned_data["dtNascimento"]

        idade = today.year - dtNascimentoAux.year - ((today.month, today.day) < (dtNascimentoAux.month, dtNascimentoAux.day))

        if idade < 18:
            raise ValidationError('Permitido apenas para pessoas maiores de 18 anos.')

        return self.cleaned_data["dtNascimento"]
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
        exclude = ['user', 'email', 'ativo', 'dt_inclusao', 'senha']


class UsuarioRedeSocialForm(ModelForm):

    class Meta:
        model = Usuario_RedeSocial
        exclude = ['user', 'dt_inclusao']


class InformeForm(ModelForm):
    texto = forms.CharField(label='Texto:', max_length=3000,widget=forms.Textarea(attrs={'size': '40'}))
    dtExpiracao = forms.DateField(label='Data de Expiração', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Informe
        exclude = ['user', 'dt_inclusao']


class EmpresaForm(ModelForm):
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), required=False, widget = forms.Select(attrs={'class': "selEstado"}))

    class Meta:
        model = Empresa
        exclude = ['dt_inclusao']


class Usuario_EmpresaForm(ModelForm):
    dtInicio = forms.DateField(label='Dt. Contratação:', required=True, widget=DateInput(attrs={'type': 'date'}))
    dtFim = forms.DateField(label='Dt. Rescisão:', required=False, widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Usuario_Empresa
        exclude = ['user', 'empresa', 'dt_inclusao']


class GraduacaoForm(ModelForm):
    dtInicio = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    dtFim = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Usuario_Graduacao
        exclude = ['user', 'curso', 'dtInclusao']



class PosForm(ModelForm):
    dtInicio = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    dtFim = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Usuario_Pos
        exclude = ['user', 'dt_inclusao']
