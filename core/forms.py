# core/forms.py

from django import forms
from .models import Empresa, Cliente, Entrada, Saida, Funcionario

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome_empresa', 'cnpj']
        widgets = {
            'nome_empresa': forms.TextInput(attrs={'placeholder': 'Ex: Nome da Empresa Ltda.'}),
            'cnpj': forms.TextInput(attrs={'placeholder': '00.000.000/0000-00'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome_cliente', 'cpf', 'empresa']
        widgets = {
            'nome_cliente': forms.TextInput(attrs={'placeholder': 'Ex: João da Silva'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
        }

class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ['nome', 'valor', 'quantidade', 'empresa_fornecedora', 'cliente', 'descricao', 'data']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Detalhes sobre o custo ou compra...'}),
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

class SaidaForm(forms.ModelForm):
    class Meta:
        model = Saida
        fields = ['nome', 'valor', 'entradas_relacionadas', 'descricao', 'data']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Detalhes sobre a venda ou serviço...'}),
            'data': forms.DateInput(attrs={'type': 'date'}),
            # Melhora a seleção de múltiplos itens, trocando a lista por checkboxes
            'entradas_relacionadas': forms.CheckboxSelectMultiple,
        }

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'salario', 'pagamento_efetuado', 'data_pagamento']
        widgets = {
            # O campo BooleanField já renderiza um checkbox por padrão
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
        }