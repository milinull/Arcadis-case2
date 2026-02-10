from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
import pandas as pd
import tempfile
import os

from .models import AvaliacaoRisco
from .serializers import AvaliacaoRiscoSerializer
from .utils import processar_dataframe, gerar_relatorio_excel


class AvaliacaoRiscoViewSet(viewsets.ModelViewSet):
    # Ordena pelo mais recente
    queryset = AvaliacaoRisco.objects.all().order_by("id")
    serializer_class = AvaliacaoRiscoSerializer


class UploadRiskView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({"error": "Nenhum arquivo enviado"}, status=status.HTTP_400_BAD_REQUEST)

        # Salva arquivo temporário para leitura
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            for chunk in file_obj.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            # Processa o DataFrame
            df = processar_dataframe(tmp_path)

            # Prepara os dados para inserção no banco
            df_banco = df.replace({pd.NA: None, float('nan'): None, "-": None})
            
            objetos_para_criar = []
            for _, row in df_banco.iterrows():
                obj = AvaliacaoRisco(
                    cas=row.get("CAS"),
                    contaminante=row.get("CONTAMINANTE"),
                    efeito=row.get("EFEITO"),
                    ambientes_abertos=row.get("AMBIENTES ABERTOS"),
                    ambientes_fechados=row.get("AMBIENTES FECHADOS"),
                    vor_nome=row.get("VOR"),
                    valor_vor=row.get("Valor VOR (mg/l)"),
                    solubilidade=500,
                    menor_valor_final=row.get("MENOR VALOR FINAL"),
                    is_cinza=bool(row.get("Cinza", False)),
                    is_laranja=bool(row.get("Laranja", False))
                )
                objetos_para_criar.append(obj)
            
            # Insere no banco
            AvaliacaoRisco.objects.bulk_create(objetos_para_criar)

            # Gera o Excel de retorno
            excel_file = gerar_relatorio_excel(df)

            response = HttpResponse(
                excel_file.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="Analise_Risco_{file_obj.name}"'
            
            return response

        except Exception as e:
            return Response({
                "error": str(e),
                "type": type(e).__name__
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)