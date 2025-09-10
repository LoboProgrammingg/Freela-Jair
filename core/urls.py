from django.urls import path
from django.views.generic import RedirectView
from .views import (
    EmpresaListView, EmpresaCreateView, EmpresaUpdateView, EmpresaDeleteView,
    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
)

urlpatterns = [
    # Redireciona a raiz do site para a lista de clientes
    path('', RedirectView.as_view(pattern_name='cliente-list', permanent=False)),

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
]