from django.db import models


class Contaminante(models.Model):

    # Colunas do banco (Tabela Contaminante)
    cas = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=250)

    class Meta:
        db_table = "contaminante"


class AvaliacaoRisco(models.Model):

    # Colunas do banco (Tabela AvaliacaoRisco)
    contaminante = models.ForeignKey(
        Contaminante, on_delete=models.CASCADE, db_column="contaminante_id"
    )
    efeito = models.CharField(max_length=2)
    ambiente = models.CharField(max_length=15)
    vor = models.CharField(max_length=150, null=True, blank=True)
    valor_vor = models.DecimalField(max_digits=20, decimal_places=15)
    concentracao_max = models.DecimalField(max_digits=20, decimal_places=15)
    solu_concentracao = models.PositiveIntegerField(default=500)

    class Meta:
        db_table = "avaliacao_risco"


class AnaliseProcess(models.Model):

    # Colunas do banco (VIEW)
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
        db_table = 'case2"."vw_analise_processada'
        managed = False
