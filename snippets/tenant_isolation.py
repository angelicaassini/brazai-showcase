"""
BrazAI — Isolamento multi-tenant (trecho curado do repositório privado).

Toda ViewSet que herda este mixin passa a filtrar os dados pelo restaurante
(tenant) do usuário logado e injeta o tenant ao criar registros.
Isolamento por construção: um restaurante nunca enxerga os dados de outro.
"""
from rest_framework.exceptions import PermissionDenied


class TenantFilterMixin:
    """Garante isolamento por tenant em ViewSets/Generics."""

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and getattr(user, 'tenant_id', None):
            return queryset.filter(tenant=user.tenant)
        return queryset.none()

    def perform_create(self, serializer):
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant is None:
            raise PermissionDenied('Sua conta não está vinculada a um restaurante.')
        serializer.save(tenant=tenant)
