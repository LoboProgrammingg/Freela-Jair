# core/models.py
from django.db import models

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