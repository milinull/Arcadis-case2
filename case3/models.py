from django.db import models


class DadosColetados(models.Model):

    # Colunas do banco (Tabela dados_coletados)
    id = models.AutoField(primary_key=True)
    sys_loc_code = models.CharField(max_length=100)
    param_code = models.CharField(max_length=50)
    param_value = models.JSONField()
    param_unit = models.CharField(max_length=50)
    measurement_method = models.CharField(max_length=250)
    measurement_date = models.DateTimeField()
    remark = models.CharField(max_length=150)
    task_code = models.CharField(max_length=250)

    class Meta:
        db_table = 'dados_coletados'