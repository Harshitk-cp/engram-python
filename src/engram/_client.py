"""Core HTTP client for the Engram SDK."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional, Type, TypeVar

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    ConflictError,
    ConnectionError,
    NotFoundError,
    ServerError,
    ValidationError,
)

T = TypeVar("T")

_ERROR_MAP: Dict[int, Type[APIError]] = {
    400: ValidationError,
    401: AuthenticationError,
    404: NotFoundError,
    409: ConflictError,
}


class _BaseClient:
    """Shared logic for sync and async clients."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        resolved_url = base_url or os.environ.get("ENGRAM_BASE_URL")
        if not resolved_url:
            raise ValueError(
                "base_url is required. Pass it explicitly or set the ENGRAM_BASE_URL environment variable."
            )
        self.base_url = resolved_url.rstrip("/")
        self.api_key = api_key or os.environ.get("ENGRAM_API_KEY")
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _handle_response(self, response: httpx.Response) -> Any:
        if response.status_code == 204:
            return None

        body: Any = None
        try:
            body = response.json()
        except Exception:
            body = response.text

        if response.is_success:
            return body

        message = ""
        if isinstance(body, dict):
            message = body.get("error", str(body))
        else:
            message = str(body)

        exc_cls = _ERROR_MAP.get(response.status_code, APIError)
        if response.status_code >= 500:
            exc_cls = ServerError

        raise exc_cls(message=message, status_code=response.status_code, body=body)


class SyncHTTPClient(_BaseClient):
    """Synchronous HTTP client."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        super().__init__(base_url, api_key, timeout)
        self._client = http_client or httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
        )
        self._owns_client = http_client is None

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        headers = self._headers()
        if extra_headers:
            headers.update(extra_headers)
        try:
            response = self._client.request(
                method, path, json=json, params=params, headers=headers
            )
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to {self.base_url}: {e}") from e
        return self._handle_response(response)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()


class AsyncHTTPClient(_BaseClient):
    """Asynchronous HTTP client."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        super().__init__(base_url, api_key, timeout)
        self._client = http_client or httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
        )
        self._owns_client = http_client is None

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        headers = self._headers()
        if extra_headers:
            headers.update(extra_headers)
        try:
            response = await self._client.request(
                method, path, json=json, params=params, headers=headers
            )
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to {self.base_url}: {e}") from e
        return self._handle_response(response)

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()
