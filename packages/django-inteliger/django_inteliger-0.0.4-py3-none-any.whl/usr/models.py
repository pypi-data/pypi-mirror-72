from django.db import models
import core.models
from django.contrib.auth.models import AbstractUser
from compositefk.fields import CompositeForeignKey


class Profile(AbstractUser, core.models.Log):
    nm_completo = models.CharField(max_length=200, null=True)

    tipo_codigo = models.CharField(null=True, max_length=200)
    tipo_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE.TIPO')
    tipo = CompositeForeignKey(core.models.Tipo, on_delete=models.DO_NOTHING, null=True, related_name='usr_profile_tipo', to_fields={
        "codigo": "tipo_codigo",
        "tipo": "tipo_tipo"
    })

    class Meta:
        db_table = 'profile'
        managed = False


class Grupo(core.models.Log):
    nivel = models.IntegerField(null=True)
    ist_login = models.BooleanField(null=True)
    ist_staff = models.BooleanField(default=False)
    nome = models.CharField(max_length=200, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    descricao = models.CharField(max_length=500, null=True)
    usr = models.ManyToManyField('Profile', through='GrupoUser', through_fields=('grupo', 'usr'))

    class Meta:
        db_table = 'grupo'
        managed = False


class GrupoUser(core.models.Log):
    grupo = models.ForeignKey('Grupo', on_delete=models.DO_NOTHING)
    usr = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    ist_admin = models.BooleanField(default=False, null=True)
    dt_ini = models.DateField(null=True)
    dt_fim = models.DateField(null=True)

    class Meta:
        db_table = 'grupouser'
        managed = False


class GrupoLogin(core.models.Log):
    sistema = models.ForeignKey('core.Sistema', null=True, on_delete=models.DO_NOTHING)
    grupo = models.ForeignKey('Grupo', on_delete=models.DO_NOTHING)
    view_inicial = models.CharField(max_length=200, null=True)
    cod_1 = models.CharField(max_length=50, null=True)
    cod_2 = models.CharField(max_length=50, null=True)
    cod_3 = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'grupologin'
        managed = False


class PontoFuncao(core.models.Log):
    sistema = models.ForeignKey('core.Sistema', null=True, on_delete=models.DO_NOTHING)
    acao = models.CharField(max_length=100, primary_key=True)
    codigo = models.IntegerField(null=True)

    versao = models.CharField(max_length=10, null=True)
    descricao = models.CharField(max_length=500, null=True)

    modulo = models.CharField(max_length=100, null=True)
    pagina = models.CharField(max_length=100, null=True)
    lugares = models.TextField(null=True)

    class Meta:
        db_table = 'pontofuncao'
        managed = False


class PontoFuncaoRelacao(core.models.Log):
    pontofuncao = models.ForeignKey('PontoFuncao', null=True, on_delete=models.DO_NOTHING)
    codigo = models.CharField(max_length=200, null=True)
    tipo = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'pontofuncaorelacao'
        managed = False