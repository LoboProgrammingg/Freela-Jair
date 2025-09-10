# core/models.py
from django.db import models
from django.utils import timezone

class Empresa(models.Model):
    nome_empresa = models.CharField(max_length=200, verbose_name="Nome da Empresa")
    cnpj = models.CharField(max_length=18, blank=True, null=True, verbose_name="CNPJ")

    def __str__(self):
        return self.nome_empresa

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nome_empresa']


class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=200, verbose_name="Nome do Cliente")
    cpf = models.CharField(max_length=14, blank=True, null=True, verbose_name="CPF")
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Empresa")

    def __str__(self):
        return self.nome_cliente

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome_cliente']

class Entrada(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome da Entrada/Custo")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    # Relacionamentos opcionais
    empresa_fornecedora = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Empresa Fornecedora")
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente Associado")
    
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    data = models.DateField(default=timezone.now, verbose_name="Data")

    def __str__(self):
        return f"{self.nome} - R$ {self.valor}"

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"
        ordering = ['-data']


class Saida(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome da Saída/Venda")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Venda")
    # Relacionamento Muitos-para-Muitos com Entrada
    entradas_relacionadas = models.ManyToManyField(Entrada, blank=True, verbose_name="Custos/Entradas Relacionados")
    
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    data = models.DateField(default=timezone.now, verbose_name="Data")

    def custo_total_entradas(self):
        """Soma o valor de todas as entradas relacionadas."""
        return sum(entrada.valor * entrada.quantidade for entrada in self.entradas_relacionadas.all())

    @property
    def lucro_bruto(self):
        """Calcula o lucro bruto da saída."""
        custo = self.custo_total_entradas()
        return self.valor - custo

    @property
    def margem_lucro_percentual(self):
        """Calcula a margem de lucro em porcentagem."""
        custo = self.custo_total_entradas()
        lucro = self.lucro_bruto

        if custo > 0:
            # Fórmula: (lucro / custo) * 100
            return (lucro / custo) * 100
        
        # Se não há custo (mão de obra pura), o lucro é 100% do valor da venda.
        # A margem é tecnicamente infinita, mas para o usuário, "100% de Lucro" faz mais sentido.
        if lucro > 0:
            return 100.00 # Representa 100% de lucro sobre o valor da venda
        
        return 0.0

    def __str__(self):
        return f"{self.nome} - R$ {self.valor}"

    class Meta:
        verbose_name = "Saída"
        verbose_name_plural = "Saídas"
        ordering = ['-data']