import requests
from requests import Response


class SessionWithTimeOut(requests.Session):
    def __init__(self, timeout: int):
        super().__init__()
        self.timeout = timeout

    def request(self, *args, **kwargs) -> Response:
        timeout = kwargs.pop("timeout", int(self.timeout))
        return super().request(*args, **kwargs, timeout=timeout)
