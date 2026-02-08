from rest_framework import serializers
from .models import DadosColetados


class DadosColetadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosColetados
        fields = "__all__"

