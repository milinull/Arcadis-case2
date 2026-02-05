from django.db import models


class AnaliseProcess(models.Model):

    # Colunas do banco
    id = models.IntegerField(primary_key=True)
    cas = models.CharField(max_length=50)
    nome = models.CharField(max_length=250)
    efeito = models.CharField(max_length=2)
    ambiente = models.CharField(max_length=15)
    vor = models.CharField(max_length=150)
    valor_vor = models.DecimalField(max_digits=20, decimal_places=15)
    concentracao_max = models.DecimalField(max_digits=20, decimal_places=15)
    solu_concentracao = models.PositiveIntegerField()
    valor_considerado = models.DecimalField(max_digits=20, decimal_places=15)
    valor_final = models.DecimalField(max_digits=20, decimal_places=15)
    aplicar_cinza = models.BooleanField()
    aplicar_laranja = models.BooleanField()

    class Meta:
        db_table = "vw_analise_processada"
        managed = False
