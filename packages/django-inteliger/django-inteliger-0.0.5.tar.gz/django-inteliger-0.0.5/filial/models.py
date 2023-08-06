from compositefk.fields import CompositeForeignKey
from django.db import models
import core.models
# Create your models here.


class Filial(core.models.EmpresaLog, core.models.Endereco):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200, null=True)
    nome_completo = models.CharField(max_length=200, null=True)
    cnpj = models.CharField(max_length=50, null=True)
    telefone = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=200, null=True)

    servicos = models.ManyToManyField('Servico', through='FilialServico', through_fields=('filial', 'servico'))

    class Meta(core.models.Endereco.Meta):
        abstract = False
        db_table = 'filial'


class Servico(core.models.Log):
    nome = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)

    tipo_codigo = models.CharField(null=True, max_length=200)
    tipo_tipo = models.CharField(null=True, max_length=200, default='FILIAL.SERVICO.TIPO')
    tipo = CompositeForeignKey(core.models.Tipo, on_delete=models.DO_NOTHING, null=True, related_name='filial_servico_tipo', to_fields={
        "codigo": "tipo_codigo",
        "tipo": "tipo_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial_servico'


class FilialServico(core.models.Log):
    servico = models.ForeignKey('Servico', on_delete=models.DO_NOTHING, null=True)
    filial = models.ForeignKey('Filial', on_delete=models.DO_NOTHING, to_field='codigo', null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial_filialservico'
