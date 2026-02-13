"""Tenant resource."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..types import Tenant

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class Tenants:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def create(self, name: str) -> Tenant:
        """Create a new tenant and receive an API key.

        This is the bootstrap endpoint — no authentication required.
        """
        data = self._client.request("POST", "/v1/tenants", json={"name": name})
        return Tenant.model_validate(data)


class AsyncTenants:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def create(self, name: str) -> Tenant:
        data = await self._client.request("POST", "/v1/tenants", json={"name": name})
        return Tenant.model_validate(data)
