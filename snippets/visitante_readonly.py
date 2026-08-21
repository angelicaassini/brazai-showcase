"""
BrazAI — Modo visitante / somente leitura (trecho curado do repositório privado).

É a trava por trás do botão "Entrar como visitante" da demo: um usuário com
`is_readonly=True` VÊ tudo (GET), mas qualquer POST/PUT/PATCH/DELETE é barrado
AQUI, no middleware, ANTES da view. Feito no middleware (e não numa permissão do
DRF) de propósito: assim a regra vale para TODAS as rotas, inclusive as que
definem suas próprias `permission_classes`. Recrutadores exploram o app por
dentro sem bagunçar os dados.
"""
from django.http import JsonResponse
from rest_framework.permissions import SAFE_METHODS
from rest_framework_simplejwt.authentication import JWTAuthentication

# Rotas de auth que aceitam escrita mesmo do visitante (login/refresh/logout).
_EXEMPT_PATHS = frozenset({
    '/api/v1/auth/login/', '/api/v1/auth/register/',
    '/api/v1/auth/refresh/', '/api/v1/auth/logout/',
})
_MESSAGE = 'Modo visitante: demonstração somente leitura. Criar/editar/excluir desabilitados.'


class ReadOnlyVisitorMiddleware:
    """Barra escritas de usuários `is_readonly` em toda a API."""

    def __init__(self, get_response):
        self.get_response = get_response
        self._jwt = JWTAuthentication()

    def __call__(self, request):
        if (
            request.method not in SAFE_METHODS
            and request.path.startswith('/api/')
            and request.path not in _EXEMPT_PATHS
        ):
            try:
                result = self._jwt.authenticate(request)
            except Exception:
                result = None  # token inválido/expirado: deixa a view/DRF tratar
            if result is not None:
                user, _token = result
                if getattr(user, 'is_readonly', False):
                    return JsonResponse({'detail': _MESSAGE}, status=403)
        return self.get_response(request)
