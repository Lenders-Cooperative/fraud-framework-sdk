from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Union

from fraud_framework_sdk import errors


@dataclass(frozen=True)
class Response:
    client: Any
    api_url: str
    http_method: str
    status_code: int
    req_args: dict
    headers: dict
    data: Union[dict, bytes]
    request_time: datetime
    response_time: datetime
    elapsed_time: timedelta = field(init=False)

    def __post_init__(self):
        super().__setattr__("elapsed_time", self.response_time - self.request_time)

    def validate(self):
        """Check if the response from Fraud Framework was successful.
        Returns:
            (Response)
                This method returns it's own object. e.g. 'self'
        Raises:
            Exception: The request to the Fraud Framework API failed.
        """
        if self.status_code == 200 and isinstance(self.data, (bytes, dict)):
            return self
        msg = f"The request to the Fraud Framework API failed. (url: {self.api_url})"
        raise errors.FraudFrameworkApiError(message=msg, response=self)
