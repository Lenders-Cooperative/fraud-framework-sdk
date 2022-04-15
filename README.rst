===================
fraud-framework-sdk
===================

.. image:: https://img.shields.io/github/workflow/status/LendersCopperative/fraud-framework-sdk/main/main?style=for-the-badge
   :target: https://github.com/LendersCopperative/fraud-framework-sdk/actions?workflow=main

.. .. image:: https://img.shields.io/badge/Coverage-100%25-success?style=for-the-badge
..   :target: https://github.com/LendersCopperative/fraud-framework-sdk/actions?workflow=main

.. .. image:: https://img.shields.io/pypi/v/fraud-framework-sdk.svg?style=for-the-badge
..    :target: https://pypi.org/project/fraud-framework-sdk/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
   :target: https://github.com/psf/black


Lightweight Python wrapper to submit risk verifications requests and other actions to the Fraud Framework.

Installation
============

Use **pip**:

.. code-block:: sh

    pip install fraud-framework-sdk

Python 3.8 to 3.10 supported.


Usage
=====

Quickstart
~~~~~~~~~~
``fraud-framework-sdk`` is a lightweight Python wrapper to submit risk verifications requests and other actions to the Fraud Framework.
For example:

.. code-block:: python

    from fraud_framework_sdk import WebClient

    payload = {
        "sourceReference": "123123123",
        "validationRules": ["kyc", "doc-check", "fraud", "socure"],
        "personalInfo": {
            "firstName": "John",
            "lastName": "Doe",
            "familyName": "Doe",
            "email": "johndoe5@gmail.com",
            "phone": { "mobile": "5552228888", "office": "4365558888" },
            "id": { "ssn": "1234567890", "tin": "1234567890", "ein": "1234567890" }
        },
        "deviceInfo": { "ip": "123.123.23.2", "session": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad" },
        "businessInfo": {
            "primaryBorrowerName": "Jane Doe",
            "primaryBorrwerIndicator": "Y",
            "businessName": "Acme, LLC.",
            "tradeName": None,
            "businessType": None
        },
        "addressInfo": [
            {
            "addressType": "Permanent",
            "addressDetails": {
                "line1": "10021 1 1/2 Mile Rd",
                "line2": None,
                "city": "East Leroy",
                "state": "MI",
                "zip": "49051",
                "country": "US"
            }
            },
            {
            "addressType": "Mailing",
            "addressDetails": {
                "line1": "10021 1 1/2 Mile Rd",
                "line2": None,
                "city": "East Leroy",
                "state": "MI",
                "zip": "49051",
                "country": "US"
            }
            }
        ],
        "documentInfo": []
    }
    client = WebClient("1234567890", callback_url="http://mycallback-url.net")
    response1 = client.perform_risk_review(payload, request_id=123123123)
    print(response1.data)

    response2 = client.search_request_id(request_id=123123123)
    print(response2.data)


Local Development
~~~~~~~~~~~~~~~~~
To receive the callback from the Fraud Framework, you must first expose your localhost to the internet. This is the quickest way to get to testing without having to setup a domain with SSL first.
We highly recommend using a tool such as `ngrok <https://ngrok.com/>`_.
Ngrok will allow you to expose your localhost so you can do end-to-end testing as you develop.

After installation, run the following command in your terminal:

.. code-block:: sh

    ngrok http -host-header=rewrite localhost:[port]

Ngrok will now host your service on the internet with a custom ngrok domain. Use this domain as your ``callback_url`` in your request to the Fraud Framework.


Todo
====
- [x] Base API calls for endpoints
- [x] Add documentation
- [x] Add and validate support for Python 3.8, 3.9, 3.10
- [x] Add mock request tests
- [ ] Setup GitHub action for testing
- [x] Integrate mypy and enable type hinting
- [ ] (?) Optional JSON schema validation for request payload
