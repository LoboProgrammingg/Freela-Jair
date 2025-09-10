# core/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Empresa, Cliente, Entrada, Saida


# --- Views para Empresa ---
class EmpresaListView(ListView):
    model = Empresa
    template_name = 'core/empresa_list.html'
    context_object_name = 'empresas'

class EmpresaCreateView(CreateView):
    model = Empresa
    fields = ['nome_empresa', 'cnpj']
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('empresa-list')

class EmpresaUpdateView(UpdateView):
    model = Empresa
    fields = ['nome_empresa', 'cnpj']
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('empresa-list')

class EmpresaDeleteView(DeleteView):
    model = Empresa
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('empresa-list')

# --- Views para Cliente ---
class ClienteListView(ListView):
    model = Cliente
    template_name = 'core/cliente_list.html'
    context_object_name = 'clientes'

class ClienteCreateView(CreateView):
    model = Cliente
    fields = ['nome_cliente', 'cpf', 'empresa']
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('cliente-list')

class ClienteUpdateView(UpdateView):
    model = Cliente
    fields = ['nome_cliente', 'cpf', 'empresa']
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('cliente-list')

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('cliente-list')

class EntradaListView(ListView):
    model = Entrada
    template_name = 'core/entrada_list.html'
    context_object_name = 'entradas'

class EntradaCreateView(CreateView):
    model = Entrada
    fields = ['nome', 'valor', 'quantidade', 'empresa_fornecedora', 'cliente', 'descricao', 'data']
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('entrada-list')

class EntradaUpdateView(UpdateView):
    model = Entrada
    fields = ['nome', 'valor', 'quantidade', 'empresa_fornecedora', 'cliente', 'descricao', 'data']
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('entrada-list')

class EntradaDeleteView(DeleteView):
    model = Entrada
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('entrada-list')

# --- Views para Saída ---
class SaidaListView(ListView):
    model = Saida
    template_name = 'core/saida_list.html'
    context_object_name = 'saidas'

class SaidaCreateView(CreateView):
    model = Saida
    fields = ['nome', 'valor', 'entradas_relacionadas', 'descricao', 'data']
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('saida-list')

class SaidaUpdateView(UpdateView):
    model = Saida
    fields = ['nome', 'valor', 'entradas_relacionadas', 'descricao', 'data']
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('saida-list')

class SaidaDeleteView(DeleteView):
    model = Saida
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('saida-list')