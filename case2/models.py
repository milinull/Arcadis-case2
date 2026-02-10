from django.db import models

class AvaliacaoRisco(models.Model):

    # Colunas do banco (Tabela avaliacao_risco)
    id = models.AutoField(primary_key=True)
    cas = models.CharField(max_length=50, null=True, blank=True)
    contaminante = models.CharField(max_length=255, null=True, blank=True)
    efeito = models.CharField(max_length=2, null=True, blank=True)
    ambientes_abertos = models.FloatField(null=True, blank=True)
    ambientes_fechados = models.FloatField(null=True, blank=True)
    vor_nome = models.CharField(max_length=150, null=True, blank=True)
    valor_vor = models.FloatField(null=True, blank=True)
    solubilidade = models.IntegerField(default=500)
    menor_valor_final = models.FloatField(null=True, blank=True)
    is_cinza = models.BooleanField(default=False)
    is_laranja = models.BooleanField(default=False)

    class Meta:
        db_table = 'avaliacao_risco'