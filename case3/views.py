from rest_framework import viewsets
from django.shortcuts import render
from .models import DadosColetados
from .serializers import DadosColetadosSerializer

class DadosColetadosViewSet(viewsets.ModelViewSet):
    # Ordena pelo mais recente
    queryset = DadosColetados.objects.all().order_by("id")
    serializer_class = DadosColetadosSerializer