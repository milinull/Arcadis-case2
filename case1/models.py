from django.db import models

class ResultadosAmostras(models.Model):

    # Colunas do banco (Tabela resultados_amostras)
    id = models.AutoField(primary_key=True)
    id_interna = models.CharField(max_length=100)
    nome_amostra = models.CharField(max_length=50)
    data_coleta = models.DateField()
    horario_coleta = models.TimeField()
    param_quimi = models.CharField(max_length=100)
    resultado = models.CharField(max_length=50)
    unidade = models.CharField(max_length=50)
    limite_quant = models.IntegerField()

    class Meta:
        db_table = 'resultados_amostras'
