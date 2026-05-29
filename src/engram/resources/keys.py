"""API key management resource."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import APIKey, CreateKeyResult

if TYPE_CHECKING:
    from .._client import AsyncHTTPClient, SyncHTTPClient


class Keys:
    def __init__(self, client: SyncHTTPClient) -> None:
        self._client = client

    def create(
        self,
        name: str,
        scopes: Optional[List[str]] = None,
        expires_at: Optional[datetime] = None,
    ) -> CreateKeyResult:
        """Create a restricted API key for the authenticated tenant.

        Requires a key with ``admin`` scope.
        The returned ``api_key`` is shown only once — store it securely.

        Args:
            name: Human-readable label for the key (e.g. ``"ci-pipeline"``).
            scopes: List of scopes. Defaults to ``["read", "write"]``.
                    Valid values: ``"read"``, ``"write"``, ``"admin"``.
            expires_at: Optional expiry datetime after which the key is rejected.

        Returns:
            :class:`CreateKeyResult` containing the full key and metadata.
        """
        body: Dict[str, Any] = {"name": name}
        if scopes is not None:
            body["scopes"] = scopes
        if expires_at is not None:
            body["expires_at"] = expires_at.isoformat()

        data = self._client.request("POST", "/v1/keys", json=body)
        return CreateKeyResult.model_validate(data)

    def list(self) -> List[APIKey]:
        """List all active (non-revoked) API keys for the authenticated tenant.

        Requires a key with ``admin`` scope.
        Full key values are never returned — only prefix and metadata.
        """
        data = self._client.request("GET", "/v1/keys")
        return [APIKey.model_validate(k) for k in data.get("keys", [])]

    def revoke(self, key_id: str) -> None:
        """Revoke an API key by ID. Takes effect on the next request using that key.

        Requires a key with ``admin`` scope.
        """
        self._client.request("DELETE", f"/v1/keys/{key_id}")


class AsyncKeys:
    def __init__(self, client: AsyncHTTPClient) -> None:
        self._client = client

    async def create(
        self,
        name: str,
        scopes: Optional[List[str]] = None,
        expires_at: Optional[datetime] = None,
    ) -> CreateKeyResult:
        """Create a restricted API key. See :meth:`Keys.create` for details."""
        body: Dict[str, Any] = {"name": name}
        if scopes is not None:
            body["scopes"] = scopes
        if expires_at is not None:
            body["expires_at"] = expires_at.isoformat()

        data = await self._client.request("POST", "/v1/keys", json=body)
        return CreateKeyResult.model_validate(data)

    async def list(self) -> List[APIKey]:
        """List active keys. See :meth:`Keys.list` for details."""
        data = await self._client.request("GET", "/v1/keys")
        return [APIKey.model_validate(k) for k in data.get("keys", [])]

    async def revoke(self, key_id: str) -> None:
        """Revoke a key. See :meth:`Keys.revoke` for details."""
        await self._client.request("DELETE", f"/v1/keys/{key_id}")
