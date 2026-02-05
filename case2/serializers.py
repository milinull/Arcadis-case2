from rest_framework import serializers
from .models import AnaliseProcess


class AnaliseProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnaliseProcess
        fields = "__all__"
