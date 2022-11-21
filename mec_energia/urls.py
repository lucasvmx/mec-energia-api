from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from universities.urls import router as universities_router
from contracts.urls import router as contracts_router
from users.urls import router as users_router
from tariffs.urls import router as tariffs_router

from .schema import Schema


router = DefaultRouter()
router.registry.extend(universities_router.registry)
router.registry.extend(contracts_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(tariffs_router.registry)

schema_view =  Schema.get_schema_view()

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path(r'api/token/', views.obtain_auth_token),
    path(r'api/', include(router.urls)),
    path('api/swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
