from rest_framework import viewsets
from django.shortcuts import render
from .models import DadosColetados
from .serializers import DadosColetadosSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.http import HttpResponse
from .utils import processar_dataframe, gerar_excel_formatado
import pandas as pd


class DadosColetadosViewSet(viewsets.ModelViewSet):
    # Ordena pelo mais recente
    queryset = DadosColetados.objects.all().order_by("id")
    serializer_class = DadosColetadosSerializer


class UploadExcelView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None): 
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({"error": "Nenhum arquivo enviado"}, status=400)

        try:
            # Processa o DataFrame
            df_limpo = processar_dataframe(file_obj)

            # Prepara os dados para inserção no banco
            objetos_para_criar = []
            
            for idx, row in df_limpo.iterrows():
                obj = DadosColetados(
                    sys_loc_code=str(row['sys_loc_code']) if pd.notna(row['sys_loc_code']) else "",
                    param_code=str(row['param_code']) if pd.notna(row['param_code']) else "",
                    param_value=row['param_value'] if pd.notna(row['param_value']) else None,
                    param_unit=str(row['param_unit']) if pd.notna(row['param_unit']) else "",
                    measurement_method=str(row['measurement_method']) if pd.notna(row['measurement_method']) else "",
                    measurement_date=row['measurement_date'],
                    remark=str(row['remark']) if pd.notna(row['remark']) else "",
                    task_code=str(row['task_code']) if pd.notna(row['task_code']) else ""
                )
                objetos_para_criar.append(obj)

            # Insere no banco
            DadosColetados.objects.bulk_create(objetos_para_criar)

            # Gera o Excel de retorno
            excel_file = gerar_excel_formatado(df_limpo)

            response = HttpResponse(
                excel_file.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="dados_processados.xlsx"'
            return response

        except Exception as e:
            return Response({
                "error": str(e),
                "type": type(e).__name__
            }, status=500)