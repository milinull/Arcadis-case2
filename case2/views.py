from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse

from .models import AnaliseProcess
from .serializers import AnaliseProcessSerializer
from .utils import gerar_relatorio_excel


class AnaliseProcessViewSet(viewsets.ModelViewSet):
    # Ordena pelo mais recente
    queryset = AnaliseProcess.objects.all().order_by("id")
    serializer_class = AnaliseProcessSerializer

    pagination_class = None

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

        # Verifica se o frontend enviou uma lista de IDs (ex: ?ids=1,2,3)
        ids_param = request.query_params.get("ids")

        if ids_param:
            # Filtra apenas os IDs solicitados
            ids_list = ids_param.split(",")
            dados = dados.filter(id__in=ids_list)

        # Se não tiver dados (filtro vazio ou banco vazio), evita erro
        if not dados.exists():
            return Response(
                {"detail": "Nenhum dado encontrado para exportação."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Chama a engine de Excel (utils.py)
        excel_file = gerar_relatorio_excel(dados)

        # Retorna o arquivo
        filename = "Relatorio_Analise.xlsx"
        response = HttpResponse(
            excel_file,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response
