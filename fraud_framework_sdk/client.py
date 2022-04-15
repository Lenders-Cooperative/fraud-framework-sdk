import hashlib
import hmac
import logging
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin

import requests

from . import errors
from .internal_utils import _modify_params_for_logging, get_user_agent
from .response import Response


class BaseClient:
    BASE_URL = "https://riskapi.sbaunifiedlending.com"

    def __init__(
        self,
        token: str,
        callback_url: str,
        base_url: str = BASE_URL,
        timeout: int = 30,
        proxy: Optional[dict] = None,
        additional_headers: Optional[dict] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.token = token.strip()
        self.callback_url = callback_url
        self.base_url = base_url
        self.timeout = timeout
        self.proxy = proxy
        self.additional_headers = additional_headers or {}

        self._logger = logger if logger is not None else logging.getLogger(__name__)
        self.ALLOWED_HTTP_METHODS = ["GET", "POST"]

    def _build_auth_headers(
        self,
        token: str,
        request_id: str,
        has_json: bool,
        source_app: str = None,
        source_program: str = None,
    ) -> dict:
        """
        Helper method to construct request headers
        Args:
            token: Authentication credentials to the Fraud Framework
            request_id: Reference ID to track your verification request
            has_json: Request body has been passed in order to update header with the correct `Content-Type`
            source_app: Reference ID to track your verification request
            source_program: Reference ID to track your verification request
        Returns:
            Request Headers
        """
        headers = {
            "Authorization": token,
            "x-request-id": request_id,
            "User-Agent": get_user_agent(),
        }
        if has_json:
            headers.update({"Content-Type": "application/json;charset=utf-8"})
        if source_program:
            headers.update({"x-source-program": source_program})
        if source_app:
            headers.update({"x-source-app": source_app})
        if self.additional_headers:
            headers.update(self.additional_headers)
        return headers

    def _send_request(self, http_method, url, params, data, headers):
        """
        Abstracted out for easy mock-testing
        """
        return requests.request(
            method=http_method,
            url=url,
            params=params,
            json=data,
            headers=headers,
            timeout=self.timeout,
            proxies=self.proxy,
        )

    def _api_call(
        self,
        endpoint: str,
        request_id: str,
        *,
        source_program: Optional[str] = None,
        source_app: Optional[str] = None,
        http_method: str = "POST",
        data: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Response:
        if http_method not in self.ALLOWED_HTTP_METHODS:
            raise errors.FraudFrameworkRequestError(f"{http_method} method is not allowed")

        url = urljoin(self.base_url, endpoint)
        request_headers = self._build_auth_headers(
            token=self.token,
            request_id=request_id,
            source_program=source_program,
            source_app=source_app,
            has_json=data is not None,
        )

        request_args = {
            "headers": request_headers,
            "params": params,
            "json": data,
        }
        request_time = datetime.utcnow()

        if self._logger.level <= logging.DEBUG:
            redacted_headers = {
                k: "(redacted)" if k.lower() == "authorization" else v for k, v in request_headers.items()
            }
            self._logger.debug(
                f"Sending a request - url: {url}, "
                f"query_params: {_modify_params_for_logging(params)}, "
                f"json_body: {data}, "
                f"headers: {redacted_headers}"
            )

        response = self._send_request(
            http_method=http_method,
            url=url,
            params=params,
            data=data,
            headers=request_headers,
        )
        response_body = response.json()
        response_time = datetime.utcnow()

        return Response(
            client=self,
            http_method=http_method,
            api_url=url,
            req_args=request_args,
            data=response_body,
            headers=dict(response.headers),
            status_code=response.status_code,
            request_time=request_time,
            response_time=response_time,
        ).validate()

    @staticmethod
    def validate_signature(*, signing_secret: str, data: str, timestamp: str, signature: str) -> bool:
        """
        Args:
            signing_secret: Your application's signing secret
            data: The raw body of the incoming request - no headers, just the body.
            timestamp: from the response header
            signature: from the response header - the calculated signature
                should match this.
        Returns:
            True if signatures matches
        """
        format_req = str.encode(f"v0:{timestamp}:{data}")
        encoded_secret = str.encode(signing_secret)
        request_hash = hmac.new(encoded_secret, format_req, hashlib.sha256).hexdigest()
        calculated_signature = f"v0={request_hash}"
        return hmac.compare_digest(calculated_signature, signature)


class WebClient(BaseClient):
    def perform_risk_review(
        self,
        data,
        request_id,
        source_app=None,
        source_program=None,
        callback_url=None,
        **kwargs,
    ) -> Response:
        """
        Args:
            data: The raw body of the incoming request - no headers, just the body.
            request_id: Reference ID to track your verification request
            source_app: Reference ID to track your verification request
            source_program: Reference ID to track your verification request
            callback_url: Callback URL that the Fraud Framework will ping back.
            kwargs:
        Returns:
            Response object
        """
        kwargs.update({"callbackUrl": callback_url or self.callback_url})
        return self._api_call(
            "/default/DoRiskReviewAPI",
            data=data,
            request_id=request_id,
            source_app=source_app,
            source_program=source_program,
            params=kwargs,
        )

    def search_request_id(self, request_id, *args, **kwargs) -> Response:
        """
        Args:
            request_id: Reference ID to track your verification request
            kwargs: Extra query params that can be passed in the request
        Returns:
            Response object
        """
        return self._api_call(f"/entities/app/ref/{request_id}", request_id, params=kwargs)
