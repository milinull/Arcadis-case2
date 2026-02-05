from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnaliseProcessViewSet

router = DefaultRouter()
router.register(r"analise", AnaliseProcessViewSet)

urlpatterns = [path("", include(router.urls))]
