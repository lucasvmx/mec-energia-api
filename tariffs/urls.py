from rest_framework.routers import DefaultRouter

from tariffs import views

router = DefaultRouter()

router.register(r'distributors', views.DistributorViewSet)
router.register(r'tariffs', views.TariffViewSet)
