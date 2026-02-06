from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse

from .models import AnaliseProcess
from .serializers import AnaliseProcessSerializer
from .utils import gerar_relatorio_excel


class AnaliseProcessViewSet(viewsets.ModelViewSet):
    # Ordena pelo mais recente
    queryset = AnaliseProcess.objects.all().order_by("-id")
    serializer_class = AnaliseProcessSerializer

    def create(self, request, *args, **kwargs):

        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, methods=["get"], url_path="exportar-excel")
    def exportar_excel(self, request):
        # Busca os dados do banco
        dados = self.get_queryset()

        # Chama a engine de Excel (utils.py)
        excel_file = gerar_relatorio_excel(dados)

        # Retorna o arquivo para o navegador
        filename = "Relatorio_Analise.xlsx"
        response = HttpResponse(
            excel_file,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response
