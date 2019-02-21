# -*- coding: utf-8 -*-
'''
Invoices Model

Classes:
    - Address: Address where the service will be executed
    - Equipment: What equipment has issues
    - Client: Who is the client
    - Supply: Materials and Services 
    - Invoice: Document with all information needed by client to confirm service payment
'''
# django imports
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

INVOICE_STATUS = (
    ('Pendente', 'Pendente'),
    ('Em Aberto', 'Em Aberto'),
    ('Paga', 'Paga'),
)

TYPE_OF_INVOICE = (
    ('Contrato', 'Contrato'),
    ('Fatura', 'Fatura'),
    ('Garantia', 'Garantia'),
    ('Instalação', 'Instalação'),
)

UNIT = (
    ('Kilômetro(s)', 'Kilômetro(s)'),
    ('Kilograma(s)', 'Kilograma(s)'),
    ('Unidade(s)', 'Unidade(s)'),
    ('Hora(s)', 'Hora(s)'),
)


class Address(models.Model):
    public_place_type = models.CharField(max_length=255, verbose_name="Tipo de Lougradoudo")
    public_place_name = models.CharField(max_length=255, verbose_name="Lougradouro")
    number = models.CharField(max_length=255, verbose_name="Número")
    sector = models.CharField(max_length=255, verbose_name="Setor/Bairro")
    complement = models.CharField(max_length=255, verbose_name="Complemento", blank=True)
    zip_code = models.CharField(max_length=8, verbose_name="CEP", validators=[MinLengthValidator(8)])
    city = models.CharField(max_length=255, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado", validators=[MinLengthValidator(2)])

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

    class Meta:
        db_table = 'equipment'
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'

    def __str__(self):
        return f'{self.type_of_equipment}, {self.manufacture}/{self.model}'


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="Cliente")
    trading_name = models.CharField(max_length=255, verbose_name="Nome Fantasia")
    contact = models.CharField(max_length=255, verbose_name="Contato")
    contact_sector = models.CharField(max_length=255, verbose_name="Setor")
    phone = models.CharField(max_length=11, verbose_name="Telefone", validators=[MinLengthValidator(11)])
    national_legal_number = models.CharField(max_length=14, verbose_name="CNPJ", validators=[MinLengthValidator(14)])
    state_legal_number = models.CharField(max_length=255, verbose_name="Inscrição Estadual", blank=True, null=True)

    class Meta:
        db_table = 'client'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.name


class Supply(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Data")
    description = models.TextField(verbose_name="Materiais/Serviços")
    amount = models.FloatField(verbose_name="Quantidade")
    unit = models.CharField(max_length=255, choices=UNIT, verbose_name="Unidade de Medida")
    value = models.FloatField(verbose_name="Valor Unitário")
    invoice_parent = models.ForeignKey('invoices.invoice', on_delete=models.DO_NOTHING, verbose_name="Ordem de Serviço", blank=True, null=True)

    class Meta:
        db_table = 'supply'
        verbose_name = 'Material/Serviço'
        verbose_name_plural = 'Materiais/Serviços'

    def __str__(self):
        return f'{self.id}: {self.description}'


class Invoice(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Data")
    client = models.ForeignKey('invoices.client', on_delete=models.DO_NOTHING, verbose_name="Cliente")
    service_address = models.ForeignKey('invoices.address', on_delete=models.DO_NOTHING, verbose_name="Endereço")
    equipment = models.ForeignKey('invoices.equipment', on_delete=models.DO_NOTHING, verbose_name="Equipamento")
    serial_number = models.CharField(max_length=255, verbose_name="Número de Série do Equipamento", blank=True, null=True)
    issue = models.CharField(max_length=255, verbose_name="Defeito")
    type_of_invoice = models.CharField(max_length=255, choices=TYPE_OF_INVOICE, verbose_name="Tipo da Ordem de Serviço")
    invoice_description = models.TextField(verbose_name="Descrição do Serviço", blank=True)
    supplies = models.ManyToManyField('invoices.supply', verbose_name="Materiais/Serviços", blank=True)
    total_value = models.FloatField(verbose_name="Valor Total", blank=True, null=True)
    created_by = models.ForeignKey('accounts.BasicUser', on_delete=models.DO_NOTHING, verbose_name="Criada por", blank=True, null=True)
    status = models.CharField(max_length=255, choices=INVOICE_STATUS, verbose_name="Status da Ordem de Serviço", default="Pendente")

    class Meta:
        db_table = 'invoice'
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'

    def __str__(self):
        return f'{self.id}: {self.client}'