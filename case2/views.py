from django.shortcuts import render
from rest_framework import viewsets
from .models import AnaliseProcess
from .serializers import AnaliseProcessSerializer


class AnaliseProcessViewSet(viewsets.ModelViewSet):
    queryset = AnaliseProcess.objects.all()
    serializer_class = AnaliseProcessSerializer
