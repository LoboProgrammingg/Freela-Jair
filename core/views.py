from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.db.models import Sum, F
from django.utils import timezone
from datetime import date, timedelta
from django.db import models
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from collections import defaultdict

from .models import Empresa, Cliente, Entrada, Saida, Funcionario


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

# --- Views para Entrada ---
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

# --- Views para Recibo (HTML e PDF) ---
class ReciboDetailView(DetailView):
    model = Saida
    template_name = 'core/recibo.html'

class ReciboPDFView(DetailView):
    model = Saida
    template_name = 'core/recibo.html'

    def render_to_response(self, context, **response_kwargs):
        html_string = render_to_string(self.template_name, context)
        html = HTML(string=html_string)
        pdf_file = html.write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="recibo_saida_{self.object.pk}.pdf"'
        return response

# --- Views para Funcionário ---
class FuncionarioListView(ListView):
    model = Funcionario
    template_name = 'core/funcionario_list.html'
    context_object_name = 'funcionarios'

    def get_queryset(self):
        # Inicia com todos os funcionários
        queryset = super().get_queryset()
        
        # Pega o parâmetro 'status' da URL. O padrão é 'todos'.
        self.status = self.request.GET.get('status', 'todos')

        # Filtra o queryset com base no status
        if self.status == 'pago':
            queryset = queryset.filter(pagamento_efetuado=True)
        elif self.status == 'pendente':
            queryset = queryset.filter(pagamento_efetuado=False)
        
        # Se for 'todos', não faz nada e retorna todos
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # O queryset já vem filtrado pelo método get_queryset()
        funcionarios_filtrados = context['object_list']

        # Calcula os totais baseados na lista JÁ FILTRADA
        total_funcionarios = funcionarios_filtrados.count()
        custo_total_qs = funcionarios_filtrados.aggregate(custo_total=Sum('salario'))
        custo_total = custo_total_qs['custo_total'] or 0

        # Adiciona os totais e o status ativo ao contexto
        context['total_funcionarios'] = total_funcionarios
        context['custo_mensal_total'] = custo_total
        context['status_ativo'] = self.status # Envia o status para o template
        
        return context
    
@require_POST  # Garante que esta view só aceita requisições POST
def confirmar_pagamento(request, pk):
    # Busca o funcionário ou retorna um erro 404 se não existir
    funcionario = get_object_or_404(Funcionario, pk=pk)
    
    # Atualiza os campos do funcionário
    funcionario.pagamento_efetuado = True
    funcionario.data_pagamento = timezone.now().date() # Define a data de pagamento como hoje
    funcionario.save()
    
    # Redireciona de volta para a lista de funcionários
    return redirect('funcionario-list')

class FuncionarioCreateView(CreateView):
    model = Funcionario
    fields = ['nome', 'salario', 'pagamento_efetuado', 'data_pagamento']
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('funcionario-list')

class FuncionarioUpdateView(UpdateView):
    model = Funcionario
    fields = ['nome', 'salario', 'pagamento_efetuado', 'data_pagamento']
    template_name = 'core/generic_form.html'
    success_url = reverse_lazy('funcionario-list')

class HistoricoPagamentosView(ListView):
    model = Funcionario
    template_name = 'core/historico_pagamentos.html'
    context_object_name = 'pagamentos'

    def get_queryset(self):
        # Buscamos apenas funcionários com pagamento efetuado e data de pagamento definida,
        # ordenados pela data de pagamento mais recente.
        return Funcionario.objects.filter(
            pagamento_efetuado=True,
            data_pagamento__isnull=False
        ).order_by('-data_pagamento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Agrupando os pagamentos por mês e ano
        pagamentos_agrupados = defaultdict(list)
        for funcionario in context['pagamentos']:
            # Formata a data como "Setembro de 2025" para usar como chave do dicionário
            chave_mes_ano = funcionario.data_pagamento.strftime('%B de %Y').capitalize()
            pagamentos_agrupados[chave_mes_ano].append(funcionario)

        # Adiciona o dicionário agrupado ao contexto
        context['pagamentos_agrupados'] = dict(pagamentos_agrupados)
        return context

class FuncionarioDeleteView(DeleteView):
    model = Funcionario
    template_name = 'core/generic_confirm_delete.html'
    success_url = reverse_lazy('funcionario-list')

# --- VIEW DO DASHBOARD ---
class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = self.request.GET.get('periodo', 'tudo')
        today = timezone.now().date()
        start_date = None
        end_date = today

        if periodo == 'hoje':
            start_date = today
        elif periodo == 'semana':
            start_date = today - timedelta(days=today.weekday())
        elif periodo == 'mes':
            start_date = today.replace(day=1)
        elif periodo == 'ano':
            start_date = today.replace(day=1, month=1)

        saidas_qs = Saida.objects.all()
        entradas_qs = Entrada.objects.all()
        funcionarios_qs = Funcionario.objects.filter(pagamento_efetuado=True)

        if start_date:
            saidas_qs = saidas_qs.filter(data__range=[start_date, end_date])
            entradas_qs = entradas_qs.filter(data__range=[start_date, end_date])
            funcionarios_qs = funcionarios_qs.filter(data_pagamento__range=[start_date, end_date])

        total_vendas = saidas_qs.aggregate(total=Sum('valor'))['total'] or 0
        total_custos_entradas = entradas_qs.aggregate(total=Sum(F('valor') * F('quantidade')))['total'] or 0
        total_salarios_pagos = funcionarios_qs.aggregate(total=Sum('salario'))['total'] or 0
        
        custos_totais = total_custos_entradas + total_salarios_pagos
        lucro_liquido = total_vendas - custos_totais

        context['total_vendas'] = total_vendas
        context['custos_totais'] = custos_totais
        context['lucro_liquido'] = lucro_liquido
        context['periodo_ativo'] = periodo
        
        return context