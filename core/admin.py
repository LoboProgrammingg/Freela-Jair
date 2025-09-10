from django.contrib import admin
from .models import Empresa, Cliente, Entrada, Saida # Adicione Entrada e Saida

# Crie classes de Admin para melhor visualização
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'data', 'empresa_fornecedora', 'cliente')
    list_filter = ('data', 'empresa_fornecedora', 'cliente')

class SaidaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'data', 'lucro_bruto', 'margem_lucro_percentual')
    list_filter = ('data',)

# Desregistre o antigo e registre com a nova classe se necessário
# ou apenas registre os novos.
admin.site.register(Empresa)
admin.site.register(Cliente)
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(Saida, SaidaAdmin)