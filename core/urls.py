from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Configuração do Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="API de Gerenciamento de Usuários",
        default_version="v1",
        description="""
        API para gerenciamento completo de usuários, incluindo:
        - Cadastro e autenticação
        - Gerenciamento de perfil
        - Recuperação de senha
        - Ativação de conta
        """,
        terms_of_service="https://www.seusite.com/termos/",
        contact=openapi.Contact(email="contato@seusite.com"),
        license=openapi.License(name="MIT License"),
        security=[{"Bearer": []}],
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

# URLs principais
urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # APIs
    path(
        "api/",
        include(
            [
                path("contas/", include("apps.contas.api.urls")),
            ]
        ),
    ),
    # Documentação
    path(
        "docs/",
        include(
            [
                re_path(
                    r"^swagger(?P<format>\.json|\.yaml)$",
                    schema_view.without_ui(cache_timeout=0),
                    name="schema-json",
                ),
                path(
                    "swagger/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="schema-swagger-ui",
                ),
                path(
                    "redoc/",
                    schema_view.with_ui("redoc", cache_timeout=0),
                    name="schema-redoc",
                ),
            ]
        ),
    ),
]

# Configurações para ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
