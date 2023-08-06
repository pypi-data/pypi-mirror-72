from __future__ import annotations
from django.db import models
from django.utils import timezone
import time

from core.sistema import Inteliger
from django.apps import apps


class InteligerQuerySet(models.QuerySet):
    def ativos(self):
        return self.filter(status=True)

    def desabilitar(self, request_=None):
        usuario = request_.user.id if request_ is not None else None
        qs = self.update(status=False, usr_delete_id=usuario, dat_delete=timezone.now())
        return qs


class InteligerManager(models.Manager):
    def get_queryset(self):
        ini = time.time()
        qs = InteligerQuerySet(self.model)
        fim = time.time()
        tempo = Inteliger().tempo_pesquisa
        if 0 < tempo < fim - ini:
            Query = apps.get_model('log', 'Query')
            Query(
                time=fim - ini,
                query=str(qs.query)
            ).save()

        return qs

    def ativos(self):
        return self.get_queryset().ativos()

    def desabilitar(self, request_=None):
        return self.get_queryset().desabilitar(request_=request_)


class DatLog(models.Model):
    dat_insercao = models.DateTimeField(auto_now_add=True, null=True)
    dat_edicao = models.DateTimeField(auto_now=True, null=True)
    dat_delete = models.DateTimeField(null=True)

    class Meta:
        managed = False
        abstract = True


class UsrLog(models.Model):
    usr_insercao = models.ForeignKey('usr.Profile', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_usr_insercao')
    usr_edicao = models.ForeignKey('usr.Profile', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_usr_edicao')
    usr_delete = models.ForeignKey('usr.Profile', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_usr_delete')

    class Meta:
        managed = False
        abstract = True


class Log(DatLog, UsrLog):
    normal_objects = models.Manager()
    objects = InteligerManager()

    status = models.BooleanField(null=True, default=True)

    class Meta:
        managed = False
        abstract = True

    def save(self, request_=None, *args, **kwargs):
        if request_ is not None:
            if self.pk is None:
                self.usr_insercao_id = request_.user.id if request_ is not None else None
                self.dat_insercao = timezone.now()
                self.status = True
            else:
                self.usr_edicao_id = request_.user.id if request_ is not None else None
                self.dat_edicao = timezone.now()
        super(Log, self).save(*args, **kwargs)

    def desabilitar(self, request_=None, *args, **kwargs):
        self.status = False
        self.usr_delete_id = request_.user.id if request_ is not None else None
        self.dat_delete = timezone.now()
        super(Log, self).save(*args, **kwargs)


class Tipo(Log):
    codigo = models.IntegerField(null=True)
    tipo = models.CharField(max_length=200, null=True)
    nome = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'tipo'
        unique_together = ('codigo', 'tipo')



class Empresa(Log):
    nome = models.CharField(max_length=100, null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'empresa'


class EmpresaLog(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING, null=True)

    class Meta(Log.Meta):
        abstract = True


class Modulo(Log):
    nome = models.SlugField(max_length=100, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    modulo_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'modulo'


class Versao(Log):
    modulo = models.ForeignKey('core.Modulo', null=True, on_delete=models.DO_NOTHING)
    responsavel = models.ForeignKey('usr.Profile', null=True, on_delete=models.DO_NOTHING)
    dat_atualizacao = models.DateField(null=True)
    codigo = models.CharField(max_length=100, null=True)
    commit = models.CharField(max_length=50, null=True)
    descricao = models.TextField(null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'versao'



class VersaoItem(Log):
    versao = models.ForeignKey('core.Versao', null=True, on_delete=models.DO_NOTHING)
    responsavel = models.ForeignKey('usr.Profile', null=True, on_delete=models.DO_NOTHING)
    ordem = models.IntegerField(null=True)
    descricao = models.TextField(null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'versaoitem'


class Erro(Log):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'erro'


class UF(Log):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200, null=True)
    nm_abrev = models.CharField(max_length=2, null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'uf'


class Municipio(Log):
    uf = models.ForeignKey('core.UF', on_delete=models.DO_NOTHING, null=True)
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'municipio'


class Data(Log):
    anomesdia = models.IntegerField(primary_key=True)
    anomes = models.IntegerField(null=True)
    ano = models.IntegerField(null=True)

    dat_dia = models.DateTimeField(null=True)

    nr_mes = models.IntegerField(null=True)
    ds_mes = models.CharField(max_length=50, null=True)
    ds_mes_abreviado = models.CharField(max_length=3, null=True)

    nr_dia = models.IntegerField(null=True)
    ds_dia_semana = models.CharField(max_length=50, null=True)

    nr_semana_ano = models.IntegerField(null=True)
    ds_semana_ano = models.CharField(max_length=50, null=True)

    nr_semana_mes = models.IntegerField(null=True)
    ds_semana_mes = models.CharField(max_length=50, null=True)

    nr_bimestre_ano = models.IntegerField(null=True)
    ds_bimestre_ano = models.CharField(max_length=50, null=True)

    nr_trimestre_ano = models.IntegerField(null=True)
    ds_trimestre_ano = models.CharField(max_length=50, null=True)

    nr_quadrimestre_ano = models.IntegerField(null=True)
    ds_quadrimestre_ano = models.CharField(max_length=50, null=True)

    nr_semestre_ano = models.IntegerField(null=True)
    ds_semestre_ano = models.CharField(max_length=50, null=True)

    nr_primeiro_dia_anomes = models.IntegerField(null=True)

    is_ultimo_dia_mes = models.BooleanField(null=True)
    ds_feriado_nacional = models.CharField(max_length=200, null=True)

    class Meta(Log.Meta):
        abstract = False
        db_table = 'data'


class Endereco(Log):
    cep = models.CharField(max_length=10, null=True)
    municipio = models.ForeignKey('core.Municipio', on_delete=models.DO_NOTHING, null=True)
    bairro = models.CharField(max_length=100, null=True)
    rua = models.CharField(max_length=100, null=True)
    numero = models.CharField(max_length=30, null=True)
    complemento = models.CharField(max_length=100, null=True)
    ponto_referencia = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=200, null=True)
    longitude = models.CharField(max_length=200, null=True)

    class Meta(Log.Meta):
        abstract = True
