import os
from typing import Any, Callable, TypeVar

import openai
from httpx import URL, Request

from .cashu import get_token, set_token

T = TypeVar("T", openai.OpenAI, openai.AsyncOpenAI)

# TODO: add routstr specific error handling
# TODO: fetch base url using nostr discovery


def patch_openai(client: T) -> T:
    if isinstance(client, openai.OpenAI):
        client = patch_sync_client(client)  # type: ignore
    elif isinstance(client, openai.AsyncOpenAI):
        client = patch_async_client(client)  # type: ignore
    else:
        raise ValueError("Invalid client")

    if client.base_url.host == "api.openai.com":
        client.base_url = URL("https://api.routstr.com/v1")

    return client


def patch_sync_client(client: openai.OpenAI) -> openai.OpenAI:
    def prepare_request(request: Request) -> None:
        request.headers["x-cashu"] = get_token()
        request.headers.pop("Authorization", None)

    client._prepare_request = prepare_request  # type: ignore

    def modify_response(func: Callable) -> Callable:
        from openai._streaming import Stream

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            pre_response = kwargs.get("response", None)
            response = func(*args, **kwargs)
            if isinstance(response, Stream):
                set_token(response.response.headers.get("x-cashu"))
                return response
            else:
                set_token(pre_response.headers.get("x-cashu"))  # type: ignore
                return response

        return wrapper

    client._process_response = modify_response(client._process_response)  # type: ignore

    return client


def patch_async_client(client: openai.AsyncOpenAI) -> openai.AsyncOpenAI:
    async def prepare_request_async(request: Request) -> None:
        request.headers["x-cashu"] = os.environ["CASHU_TOKEN"]
        request.headers.pop("Authorization", None)

    client._prepare_request = prepare_request_async  # type: ignore

    def modify_response_async(func: Callable) -> Callable:
        from openai._streaming import AsyncStream

        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            pre_response = kwargs.get("response", None)
            response = await func(*args, **kwargs)
            if isinstance(response, AsyncStream):
                set_token(response.response.headers.get("x-cashu"))
                return response
            else:
                set_token(pre_response.headers.get("x-cashu"))  # type: ignore
                return response

        return wrapper

    client._process_response = modify_response_async(client._process_response)  # type: ignore

    return client
