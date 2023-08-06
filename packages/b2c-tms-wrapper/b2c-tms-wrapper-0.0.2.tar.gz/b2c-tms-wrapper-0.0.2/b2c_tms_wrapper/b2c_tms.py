from datetime import datetime
from http import HTTPStatus
from typing import List, Dict

from requests import adapters, Response
from shuttlis.serialization import serialize
from shuttlis.time import TimeWindow
from shuttlis.utils import group_by, Location

from b2c_tms_wrapper.error import TripNotFound, BookingNotFound, BookingNotFoundOnTrip
from b2c_tms_wrapper.models import Trip, BookingRequest, BoardingMode
from b2c_tms_wrapper.timeout import SessionWithTimeOut
from b2c_tms_wrapper.utils import auto_paginate


def _mk_exc(response: Response) -> RuntimeError:
    return RuntimeError(
        f"""
    Error from B2C TMS
    status: {response.status_code}
    error: {response.text}
    """
    )


class B2CTMS:
    def __init__(self, b2c_tms_url: str, session_timeout: int = 30):
        self._b2c_tms_url = b2c_tms_url
        self._session = SessionWithTimeOut(session_timeout)
        adapter = adapters.HTTPAdapter(pool_connections=40, max_retries=3)
        self._session.mount(adapter=adapter, prefix="http://")

    def get_trip(self, trip_id: str) -> Trip:
        url = f"{self._b2c_tms_url}/api/v1/trips/{trip_id}"
        response = self._session.get(url=url)
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise TripNotFound()
        if response.status_code != HTTPStatus.OK:
            raise _mk_exc(response)
        return Trip.from_dict(response.json()["data"])

    def update_vehicle_for_trip(
        self, trip_id: str, current_vehicle_id: str, new_vehicle_id: str
    ) -> Trip:
        url = f"{self._b2c_tms_url}/api/v1/trips/vehicle/update"
        params = dict(
            trip_id=trip_id,
            from_vehicle_id=current_vehicle_id,
            to_vehicle_id=new_vehicle_id,
        )
        response = self._session.post(url, json=serialize(params))
        if response.status_code != HTTPStatus.OK:
            raise _mk_exc(response)
        return Trip.from_dict(response.json()["data"])

    def detach_vehicle_from_trip(self, trip_id: str) -> Trip:
        url = f"{self._b2c_tms_url}/api/v1/trips/{trip_id}/vehicle/detach"
        response = self._session.post(url)
        if response.status_code != HTTPStatus.OK:
            raise _mk_exc(response)
        return Trip.from_dict(response.json()["data"])

    def attach_vehicle_to_trip(self, trip_id: str, vehicle_id: str) -> Trip:
        url = f"{self._b2c_tms_url}/api/v1/trips/{trip_id}/vehicle"
        params = dict(id=vehicle_id)
        response = self._session.post(url, json=serialize(params))
        if response.status_code != HTTPStatus.OK:
            raise _mk_exc(response)
        return Trip.from_dict(response.json()["data"])

    def get_trips(self, route_ids: List[str], time_window: TimeWindow) -> List[Trip]:
        url = f"{self._b2c_tms_url}/api/v2/trips"
        query_params = serialize(
            {
                "route_ids": ",".join(route_ids),
                "from_time": time_window.from_date,
                "to_time": time_window.to_date,
            }
        )
        trips = auto_paginate(
            session=self._session, service_name="B2c TMS", url=url, params=query_params
        )
        return [Trip.from_dict(trip) for trip in trips]

    def get_booking_requests_for_trips(self, trips_ids: List[str]) -> Dict[str, List]:
        if not trips_ids:
            return {}

        url = f"{self._b2c_tms_url}/api/v1/booking_requests/by_trips"
        response = self._session.get(url=url, json={"trip_ids": serialize(trips_ids)})
        if response.status_code == HTTPStatus.OK:
            booking_requests = [
                BookingRequest.from_dict(br) for br in response.json()["data"]
            ]
            return group_by(booking_requests, lambda br: br.trip_id)
        raise _mk_exc(response)

    def board(
        self, trip_id: str, time: datetime, location: Location, mode: BoardingMode
    ) -> dict:
        url = f"{self._b2c_tms_url}/api/v1/booking_requests/board"
        params = dict(trip_id=trip_id, time=time, location=location, mode=mode)
        response = self._session.post(url, json=serialize(params))
        if response.status_code == HTTPStatus.OK:
            return response.json()["data"]
        if response.status_code == HTTPStatus.BAD_REQUEST:
            error_type = response.json()["error"]["type"]
            if error_type == "BOOKING_NOT_FOUND":
                raise BookingNotFound()
            if error_type == "BOOKING_NOT_FOUND_ON_TRIP":
                raise BookingNotFoundOnTrip()
            if error_type == "TRIP_NOT_FOUND":
                raise TripNotFound()

        raise _mk_exc(response)
