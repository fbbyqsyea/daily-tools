import asyncio
import httpx
from typing import Any, Dict, Optional

# ===== 全局配置 =====
DEFAULT_TIMEOUT: float = 60.0
MAX_RETRIES: int = 3
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
RETRY_METHODS = {"HEAD", "GET", "OPTIONS", "POST", "PUT"}


# ===== 工具函数 =====
def _parse_json_response(response: httpx.Response) -> Dict[str, Any]:
    """安全解析 JSON 响应，允许 204 或空 body"""
    if response.status_code == 204 or not response.content:
        return {}
    try:
        return response.json()
    except ValueError as e:
        snippet = response.text[:200].replace("\n", " ")
        raise ValueError(f"Invalid JSON response: {snippet}...") from e


# ===== 同步请求封装 =====
def _sync_request(
    method: str,
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Optional[float] = DEFAULT_TIMEOUT,
    retries: int = MAX_RETRIES,
) -> Dict[str, Any]:
    attempt = 0
    while attempt <= retries:
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json,
                    headers=headers,
                )
                # 仅对指定状态码重试
                if (
                    response.status_code in RETRY_STATUS_CODES
                    and method in RETRY_METHODS
                    and attempt < retries
                ):
                    raise httpx.HTTPStatusError(
                        "Retriable HTTP status",
                        request=response.request,
                        response=response,
                    )
                response.raise_for_status()
                return _parse_json_response(response)

        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            attempt += 1
            if attempt > retries:
                raise RuntimeError(
                    f"Sync HTTP request failed after {retries + 1} attempts: {e}"
                ) from e
            # 同步版也使用指数退避（可选，也可直接重试）
            import time
            delay = 0.5 * (2 ** (attempt - 1))
            time.sleep(delay)


def get(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Optional[float] = DEFAULT_TIMEOUT,
    retries: int = MAX_RETRIES,
) -> Dict[str, Any]:
    return _sync_request(
        "GET", url, params=params, headers=headers, timeout=timeout, retries=retries
    )


def post(
    url: str,
    *,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Optional[float] = DEFAULT_TIMEOUT,
    retries: int = MAX_RETRIES,
) -> Dict[str, Any]:
    return _sync_request(
        "POST", url, data=data, json=json, headers=headers, timeout=timeout, retries=retries
    )


# ===== 异步请求封装 =====
async def _async_request(
    method: str,
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Optional[float] = DEFAULT_TIMEOUT,
    retries: int = MAX_RETRIES,
) -> Dict[str, Any]:
    attempt = 0
    while attempt <= retries:
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json,
                    headers=headers,
                )
                if (
                    response.status_code in RETRY_STATUS_CODES
                    and method in RETRY_METHODS
                    and attempt < retries
                ):
                    raise httpx.HTTPStatusError(
                        "Retriable HTTP status",
                        request=response.request,
                        response=response,
                    )
                response.raise_for_status()
                return _parse_json_response(response)

        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            attempt += 1
            if attempt > retries:
                raise RuntimeError(
                    f"Async HTTP request failed after {retries + 1} attempts: {e}"
                ) from e
            delay = 0.5 * (2 ** (attempt - 1))
            await asyncio.sleep(delay)


async def aget(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Optional[float] = DEFAULT_TIMEOUT,
    retries: int = MAX_RETRIES,
) -> Dict[str, Any]:
    return await _async_request(
        "GET", url, params=params, headers=headers, timeout=timeout, retries=retries
    )


async def apost(
    url: str,
    *,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: Optional[float] = DEFAULT_TIMEOUT,
    retries: int = MAX_RETRIES,
) -> Dict[str, Any]:
    return await _async_request(
        "POST", url, data=data, json=json, headers=headers, timeout=timeout, retries=retries
    )