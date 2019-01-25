# -*- coding: utf-8 -*-
# django imports
from django.conf import settings
from django.db import models


TYPE_OF_INVOICE = (
    ('Contrato', 'Contrato'),
    ('Fatura', 'Fatura'),
    ('Garantia', 'Garantia'),
    ('Instalação', 'Instalação'),
)

INVOICE_STATUS = (
    ('Pendente', 'Pendente'),
    ('Em Aberto', 'Em Aberto'),
    ('Paga', 'Paga'),
)

class Address(models.Model):
    public_place_type = models.CharField(max_length=255, verbose_name="Tipo de Lougradoudo")
    public_place_name = models.CharField(max_length=255, verbose_name="Lougradouro")
    number = models.CharField(max_length=255, verbose_name="Número")
    sector = models.CharField(max_length=255, verbose_name="Setor/Bairro")
    complement = models.CharField(max_length=255, verbose_name="Complemento", blank=True)
    zip_code = models.CharField(max_length=255, verbose_name="CEP")
    city = models.CharField(max_length=255, verbose_name="Cidade")
    state = models.CharField(max_length=255, verbose_name="Estado")

    class Meta:
        db_table = 'address'
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        full_address = f'\
            {self.public_place_type} \
            {self.public_place_name}, \
            Nº{self.number}, \
            {self.sector}, \
            {self.complement}'

        return full_address


class Equipment(models.Model):
    type_of_equipment = models.CharField(max_length=255, verbose_name="Equipamento")
    manufacture = models.CharField(max_length=255, verbose_name="Fabricante")
    model = models.CharField(max_length=255, verbose_name="Modelo")
    serial_number = models.CharField(max_length=255, verbose_name="Número de Série")

    class Meta:
        db_table = 'equipment'
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'

    def __str__(self):
        return f'{self.type_of_equipment}, {self.manufacture}/{self.model} {self.serial_number}'


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="Cliente")
    contact = models.CharField(max_length=255, verbose_name="Contato")
    address = models.ForeignKey('invoices.address', on_delete=models.DO_NOTHING, verbose_name="Endereço")
    phone = models.CharField(max_length=255, verbose_name="Telefone")
    national_legal_number = models.CharField(max_length=255, verbose_name="CNPJ")
    state_legal_number = models.CharField(max_length=255, verbose_name="Inscrição Estadual")

    class Meta:
        db_table = 'client'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.name

class Supply(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Data")
    description = models.TextField(verbose_name="Materiais/Serviços")
    value = models.FloatField(verbose_name="Valor")

    class Meta:
        db_table = 'supply'
        verbose_name = 'Material/Serviço'
        verbose_name_plural = 'Materiais/Serviços'

    def __str__(self):
        return self.description

class Invoice(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Data")
    client = models.ForeignKey('invoices.client', on_delete=models.DO_NOTHING, verbose_name="Cliente")
    equipment = models.ForeignKey('invoices.equipment', on_delete=models.DO_NOTHING, verbose_name="Equipamento")
    issue = models.CharField(max_length=255, verbose_name="Defeito")
    type_of_invoice = models.CharField(max_length=255, choices=TYPE_OF_INVOICE, verbose_name="Tipo da Ordem de Serviço")
    invoice_description = models.TextField(verbose_name="Descrição do Serviço", blank=True)
    displacement = models.IntegerField(verbose_name="Deslocamento", blank=True)
    time = models.IntegerField(verbose_name="Horas Trabalhadas")
    supplies = models.ManyToManyField('invoices.supply', verbose_name="Serviços/Materiais", blank=True)
    total_value = models.FloatField(verbose_name="Valor Total", blank=True, null=True)
    created_by = models.ForeignKey('accounts.BasicUser', on_delete=models.DO_NOTHING, verbose_name="Criada por", blank=True, null=True)
    status = models.CharField(max_length=255, choices=INVOICE_STATUS, verbose_name="Status da Ordem de Serviço")

    class Meta:
        db_table = 'invoice'
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'

    def __str__(self):
        return f'{self.client} #{self.id}'