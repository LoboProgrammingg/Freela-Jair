from django.urls import path
from django.views.generic import RedirectView
from .views import (
    EmpresaListView, EmpresaCreateView, EmpresaUpdateView, EmpresaDeleteView,
    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    EntradaListView, EntradaCreateView, EntradaUpdateView, EntradaDeleteView,
    SaidaListView, SaidaCreateView, SaidaUpdateView, SaidaDeleteView,
)

urlpatterns = [
    # Redireciona a raiz do site para a lista de clientes
    path('', RedirectView.as_view(pattern_name='saida-list', permanent=False)),

    # Rotas de Empresa
    path('empresas/', EmpresaListView.as_view(), name='empresa-list'),
    path('empresas/nova/', EmpresaCreateView.as_view(), name='empresa-create'),
    path('empresas/<int:pk>/editar/', EmpresaUpdateView.as_view(), name='empresa-update'),
    path('empresas/<int:pk>/deletar/', EmpresaDeleteView.as_view(), name='empresa-delete'),

    # Rotas de Cliente
    path('clientes/', ClienteListView.as_view(), name='cliente-list'),
    path('clientes/novo/', ClienteCreateView.as_view(), name='cliente-create'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente-update'),
    path('clientes/<int:pk>/deletar/', ClienteDeleteView.as_view(), name='cliente-delete'),

    # Rotas de Entrada
    path('entradas/', EntradaListView.as_view(), name='entrada-list'),
    path('entradas/nova/', EntradaCreateView.as_view(), name='entrada-create'),
    path('entradas/<int:pk>/editar/', EntradaUpdateView.as_view(), name='entrada-update'),
    path('entradas/<int:pk>/deletar/', EntradaDeleteView.as_view(), name='entrada-delete'),

    # Rotas de Saída
    path('saidas/', SaidaListView.as_view(), name='saida-list'),
    path('saidas/nova/', SaidaCreateView.as_view(), name='saida-create'),
    path('saidas/<int:pk>/editar/', SaidaUpdateView.as_view(), name='saida-update'),
    path('saidas/<int:pk>/deletar/', SaidaDeleteView.as_view(), name='saida-delete'),
]