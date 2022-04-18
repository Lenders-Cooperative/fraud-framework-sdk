import logging

import pytest

from fraud_framework_sdk import __version__, errors
from fraud_framework_sdk.response import Response


def test_version():
    assert len(__version__.split(".")) == 3


def test_web_client_default_attrs(client):
    assert isinstance(client.token, str)
    assert isinstance(client.callback_url, str)
    assert isinstance(client.base_url, str) and client.base_url == client.BASE_URL
    assert isinstance(client.timeout, int)
    assert isinstance(client.additional_headers, dict)
    assert isinstance(client._logger, logging.Logger)
    assert client.proxy is None


@pytest.mark.parametrize(
    "client,kwargs,expected",
    [
        (
            "client",
            {"token": 12345, "request_id": "1231312314124214", "has_json": True, "has_files": False},
            ["Authorization", "Content-Type", "User-Agent", "x-request-id"],
        ),
        (
            "client",
            {
                "token": 12345,
                "request_id": "1231312314124214",
                "source_program": "TEST",
                "has_json": True,
                "has_files": False,
            },
            [
                "Authorization",
                "Content-Type",
                "User-Agent",
                "x-request-id",
                "x-source-program",
            ],
        ),
        (
            "client",
            {
                "token": 12345,
                "request_id": "1231312314124214",
                "source_app": "123123123123",
                "has_json": True,
                "has_files": False,
            },
            [
                "Authorization",
                "Content-Type",
                "User-Agent",
                "x-request-id",
                "x-source-app",
            ],
        ),
        (
            "client",
            {
                "token": 12345,
                "request_id": "1231312314124214",
                "source_program": "TEST",
                "source_app": 123123123123,
                "has_json": True,
                "has_files": False,
            },
            [
                "Authorization",
                "Content-Type",
                "User-Agent",
                "x-request-id",
                "x-source-program",
                "x-source-app",
            ],
        ),
        (
            "client",
            {
                "token": 12345,
                "request_id": "1231312314124214",
                "source_app": None,
                "has_json": True,
                "has_files": False,
            },
            [
                "Authorization",
                "Content-Type",
                "User-Agent",
                "x-request-id",
            ],
        ),
        (
            "client",
            {
                "token": 12345,
                "request_id": "1231312314124214",
                "source_app": None,
                "has_json": False,
                "has_files": True,
            },
            [
                "Authorization",
                "User-Agent",
                "x-request-id",
                "Content-Type",
            ],
        ),
    ],
    indirect=["client"],
)
def test_auth_headers(client, kwargs, expected):
    headers = client._build_auth_headers(**kwargs)
    assert sorted(list(headers.keys())) == sorted(expected)


def test_authorized_http_methods(client):
    assert sorted(x.lower() for x in client.ALLOWED_HTTP_METHODS) == ["get", "post"]


@pytest.mark.parametrize(
    "client,http_method",
    [
        ("client", "PUT"),
        ("client", "PATCH"),
        ("client", "DELETE"),
        ("client", "HEAD"),
        ("client", "OPTIONS"),
    ],
    indirect=["client"],
)
def test_unauthorized_http_methods(client, http_method):
    assert http_method.lower() not in [x.lower() for x in client.ALLOWED_HTTP_METHODS]
    with pytest.raises(errors.FraudFrameworkRequestError):
        client._api_call("/test", request_id=1234567890, http_method=http_method)


def test_mock_perform_risk_review_method(mocker, client, response, mock_response):
    mocker.patch("fraud_framework_sdk.client.WebClient._send_request", return_value=mock_response)
    response = client.perform_risk_review(data={}, request_id=1234567890)

    assert isinstance(response, Response)
    assert response.status_code == 200
    assert response.http_method == "POST"
    assert isinstance(response.headers, dict)
    assert isinstance(response.data, dict)


def test_search_by_request_id_method(mocker, client, response, mock_response):
    mocker.patch("fraud_framework_sdk.client.WebClient._send_request", return_value=mock_response)
    response = client.search_request_id(request_id=1234567890)

    assert isinstance(response, Response)
    assert response.status_code == 200
    assert response.http_method == "POST"
    assert isinstance(response.headers, dict)
    assert isinstance(response.data, dict)


def test_search_by_request_id_method(mocker, client, response, mock_response):
    mocker.patch("fraud_framework_sdk.client.WebClient._send_request", return_value=mock_response)
    response = client.upload_document(1234567890, file=b"mock file")

    assert isinstance(response, Response)
    assert response.status_code == 200
    assert response.http_method == "POST"
    assert isinstance(response.headers, dict)
    assert isinstance(response.data, dict)
