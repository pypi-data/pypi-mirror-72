from typing import List

from requests import Response, Session


def assert_response(response: Response, service_name: str):
    if response.status_code != 200:
        raise RuntimeError(
            f"""
            Error from {service_name}
            Response Code: {response.status_code}
            Response Body:
            {response.text}
        """
        )


def auto_paginate(
    session: Session, service_name: str, url: str, params: dict = None
) -> List[dict]:
    if not params:
        params = {}

    def _iter():
        cursor = None
        while True:
            req_params = dict(params)
            if cursor:
                req_params["after"] = cursor

            response = session.get(url, params=req_params)
            assert_response(response, service_name)

            for item in response.json()["data"]:
                yield item

            cursor = response.json()["meta"]["cursor"].get("last")
            if not cursor:
                break

    return list(_iter())
