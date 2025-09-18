""" module for http requests """
from typing import Optional
import httpx
from fastapi import HTTPException, status



class Client:
    """ HTTP Request handler """
    def __init__(self, base_url: str, timeout: Optional[float | int]):
        self.__base_url = base_url
        self.__timeout = timeout

    def get(
        self, path: str = "/", params: Optional[dict] = None, headers: Optional[dict] = None
    ) -> dict:
        """
        Sends a GET request to an external service using the configured HTTP client.

        Args:
            path (str): The endpoint path to send the request to (default is "/").
            params (dict, optional): Query parameters to include in the request.
            headers (dict, optional): Custom headers to include in the request.

        Returns:
            dict: The JSON response from the external service.

        Raises:
            HTTPException: If the response contains an HTTP error status code, 
                        if the request times out, or if there is a connection error.
                - 502 Bad Gateway: When a general request error occurs.
                - 504 Gateway Timeout: When the request times out.
                - Other: Based on the status code returned from the external service.
        """
        with httpx.Client(
            base_url=self.__base_url, timeout=self.__timeout, headers=headers
        ) as client:
            try:
                response = client.get(
                    path, params=params, timeout=self.__timeout
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=exc.response.json(),
                )

            except httpx.ReadTimeout:
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail="The request to the services timedout.",
                )

            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Failed to reach external service",
                )

        return response.json()

    def post(
        self,
        path: str = "/",
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> dict:
        with httpx.Client(
            base_url=self.__base_url, timeout=self.__timeout, headers=headers
        ) as client:
            try:
                response = client.post(
                    path, data=data, json=json, timeout=self.__timeout
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=exc.response.json(),
                )

            except httpx.ReadTimeout:
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail="The request to the services timedout.",
                )

            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Failed to reach external service",
                )

        return response.json()

    def patch(
        self,
        path: str = "/",
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> dict:
        with httpx.Client(
            base_url=self.__base_url, timeout=self.__timeout, headers=headers
        ) as client:
            try:
                response = client.patch(
                    path, params=params, data=data, json=json, timeout=self.__timeout
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=exc.response.json(),
                )

            except httpx.ReadTimeout:
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail="The request to the services timedout.",
                )

            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Failed to reach external service",
                )

        return response.json()

    def put(
        self,
        path: str = "/",
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> dict:
        with httpx.Client(
            base_url=self.__base_url, timeout=self.__timeout, headers=headers
        ) as client:
            try:
                response = client.put(
                    path, params=params, json=json, timeout=self.__timeout
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=exc.response.json(),
                )

            except httpx.ReadTimeout:
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail="The request to the services timedout.",
                )

            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Failed to reach external service",
                )

        return response.json()

    def delete(
        self, path: str = "/", params: Optional[dict] = None, headers: Optional[dict] = None
    ) -> dict:
        with httpx.Client(
            base_url=self.__base_url, timeout=self.__timeout, headers=headers
        ) as client:
            try:
                response = client.delete(
                    path, params=params, timeout=self.__timeout
                )
                response.raise_for_status()

            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=exc.response.json(),
                )

            except httpx.ReadTimeout:
                raise HTTPException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    detail="The request to the services timedout.",
                )

            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Failed to reach external service",
                )

        return response.json()
