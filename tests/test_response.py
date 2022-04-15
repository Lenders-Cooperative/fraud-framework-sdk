import dataclasses
from datetime import datetime, timedelta
from typing import Union

import pytest

from fraud_framework_sdk import WebClient, errors
from fraud_framework_sdk.response import Response


def test_response_attrs(response):
    assert isinstance(response.client, WebClient)
    assert isinstance(response.api_url, str)
    assert isinstance(response.http_method, str)
    assert isinstance(response.status_code, int)
    assert isinstance(response.req_args, dict)
    assert isinstance(response.headers, dict)
    assert isinstance(response.data, Union[dict, bytes, None])
    assert isinstance(response.request_time, datetime)
    assert isinstance(response.response_time, datetime)
    assert isinstance(response.elapsed_time, timedelta)


def test_response_immutability(response):
    with pytest.raises(dataclasses.FrozenInstanceError):
        response.status_code = 400


@pytest.mark.parametrize(
    "client,data,status_code",
    [
        ("client", b"data", 200),
        ("client", bytes(1), 200),
        ("client", {"ok": True}, 200),
    ],
    indirect=["client"],
)
def test_response_validate_success(client, data, status_code):
    response_obj = Response(
        client=client,
        api_url="http://base_url.com",
        http_method="GET",
        status_code=status_code,
        req_args={},
        headers={},
        data=data,
        request_time=datetime(year=2022, month=1, day=1, hour=1),
        response_time=datetime(year=2022, month=1, day=1, hour=2),
    )
    assert response_obj.validate() == response_obj  # return self if no errors


@pytest.mark.parametrize(
    "client,data,status_code",
    [
        ("client", "data", 200),
        ("client", None, 200),
        ("client", 12345, 200),
        ("client", b"data", None),
        ("client", b"data", 403),
        ("client", b"data", 500),
        ("client", {"ok": False}, 400),
    ],
    indirect=["client"],
)
def test_response_validate_error(client, data, status_code):
    response_obj = Response(
        client=client,
        api_url="http://base_url.com",
        http_method="GET",
        status_code=status_code,
        req_args={},
        headers={},
        data=data,
        request_time=datetime(year=2022, month=1, day=1, hour=1),
        response_time=datetime(year=2022, month=1, day=1, hour=2),
    )
    with pytest.raises(errors.FraudFrameworkApiError):
        response_obj.validate()
