from datetime import datetime

import pytest
from requests import Response as RequestsResponse

from fraud_framework_sdk import WebClient
from fraud_framework_sdk.response import Response


@pytest.fixture()
def client():
    return WebClient("1234567890", callback_url="http://mycallback-url.net")


@pytest.fixture()
def response(client):
    return Response(
        client=client,
        api_url="http://base_url.com",
        http_method="GET",
        status_code=200,
        req_args={},
        headers={},
        data={"referenceId": "555", "traceId": "333"},
        request_time=datetime(year=2022, month=1, day=1, hour=1),
        response_time=datetime(year=2022, month=1, day=1, hour=2),
    )


@pytest.fixture()
def mock_response():
    mock_response = RequestsResponse()
    mock_response.status_code = 200
    mock_response.headers = {"Authorization": 1234567890}
    mock_response._content = b'{"response": "fake it till you make it"}'
    return mock_response
