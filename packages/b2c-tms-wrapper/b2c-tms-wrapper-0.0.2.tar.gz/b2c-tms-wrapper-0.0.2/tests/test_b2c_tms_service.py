import json
import random
from datetime import datetime
from typing import Tuple

import responses
from requests import PreparedRequest
from shuttlis.geography import Location
from shuttlis.serialization import serialize
from shuttlis.time import time_now, TimeWindow
from shuttlis.utils import uuid4_str

from b2c_tms_wrapper.b2c_tms import B2CTMS
from b2c_tms_wrapper.models import (
    Trip,
    TripState,
    Vehicle,
    TripTrackedWayPoint,
    Stop,
    BoardingMode,
)

b2c_tms_service = B2CTMS(b2c_tms_url="http://dummy_b2c_tms")


def trip1() -> Trip:
    return Trip(
        id="259cc1b8-5a86-4e1b-be44-2954f6ec7c49",
        route_id="4a2a0e8d-ee20-4cf8-9827-94e8f52c4af3",
        start_time=datetime.fromisoformat("2020-06-25T16:50:00+00:00"),
        state=TripState.PLANNED,
        max_bookings=20,
        vehicle=Vehicle(
            id="d824dbd6-3036-41f6-9d1e-25ea710b9d27", registration_number=None
        ),
        way_points=[
            TripTrackedWayPoint(
                id="8bca0e6f-b4c1-4002-abd1-e9b3ce88cfe2",
                stop=Stop(
                    id="5752b57f-fd85-4c3a-9f67-6b1f30e2e7d4",
                    location=Location(lat=28.58368506583371, lng=77.21241725488308),
                ),
                estimated_departure_time=datetime.fromisoformat(
                    "2020-06-25T16:50:00+00:00"
                ),
                departed_at=None,
            ),
            TripTrackedWayPoint(
                id="caf9b191-8660-4cfe-9e88-d64267369f7e",
                stop=Stop(
                    id="c8894713-07a8-4bb0-bb49-219f545bc377",
                    location=Location(lat=28.56636061941184, lng=77.20755711353199),
                ),
                estimated_departure_time=datetime.fromisoformat(
                    "2020-06-25T16:56:00+00:00"
                ),
                departed_at=None,
            ),
        ],
    )


def trip2() -> Trip:
    return Trip(
        id="039601aa-3608-419a-9b8d-b60fd8c80105",
        route_id="22f1ccd6-e7b8-4426-b67a-4c74009b8c80",
        start_time=datetime.fromisoformat("2020-04-13T05:30:00+00:00"),
        state=TripState.PLANNED,
        max_bookings=20,
        vehicle=Vehicle(
            id="d824dbd6-3036-41f6-9d1e-25ea710b9d27", registration_number="30-3456"
        ),
        way_points=[
            TripTrackedWayPoint(
                id="b92a30d4-8f61-45e5-8038-fb76c9c43541",
                stop=Stop(
                    id="e8d614eb-fd76-4ba5-b6ea-943a10b2fd5b",
                    location=Location(lat=19.1176, lng=72.906),
                ),
                estimated_departure_time=datetime.fromisoformat(
                    "2020-04-13T05:30:00+00:00"
                ),
                departed_at=None,
            ),
            TripTrackedWayPoint(
                id="4d44ea74-24d3-4e69-bf78-348e521b24e0",
                stop=Stop(
                    id="58ad12c1-12fb-49f7-9c32-11c2491ff7fa",
                    location=Location(lat=19.1364, lng=72.8296),
                ),
                estimated_departure_time=datetime.fromisoformat(
                    "2020-04-13T05:31:00+00:00"
                ),
                departed_at=None,
            ),
        ],
    )


def trip_json_from_v1_api() -> dict:
    return {
        "allocation": {
            "id": "a39c16a5-e362-4ba3-8199-9c31bb1c3f8a",
            "type": "allocation",
        },
        "booking_opening_time": "2020-06-22T02:30:00+00:00",
        "bookings": {"type": "bookings"},
        "created_at": "2020-06-23T18:31:29.726233+00:00",
        "departures": {"type": "departures"},
        "driver": None,
        "escort": None,
        "helper": None,
        "id": "259cc1b8-5a86-4e1b-be44-2954f6ec7c49",
        "max_bookings": 20,
        "path": {"type": "path"},
        "route": {"id": "4a2a0e8d-ee20-4cf8-9827-94e8f52c4af3", "type": "route"},
        "start_time": "2020-06-25T16:50:00+00:00",
        "state": "PLANNED",
        "type": "AUTOMATIC",
        "updated_at": "2020-06-23T18:31:29.726233+00:00",
        "vehicle": {"id": "d824dbd6-3036-41f6-9d1e-25ea710b9d27", "type": "vehicle"},
        "way_points": [
            {
                "departure_time": "2020-06-25T16:50:00+00:00",
                "id": "8bca0e6f-b4c1-4002-abd1-e9b3ce88cfe2",
                "stop": {
                    "id": "5752b57f-fd85-4c3a-9f67-6b1f30e2e7d4",
                    "location": {"lat": 28.58368506583371, "lng": 77.21241725488308},
                },
                "type": "PICKUP",
            },
            {
                "departure_time": "2020-06-25T16:56:00+00:00",
                "id": "caf9b191-8660-4cfe-9e88-d64267369f7e",
                "stop": {
                    "id": "c8894713-07a8-4bb0-bb49-219f545bc377",
                    "location": {"lat": 28.56636061941184, "lng": 77.20755711353199},
                },
                "type": "DROP",
            },
        ],
    }


def trip_json_from_v2_api() -> dict:
    return {
        "booking_opening_time": "2020-04-11T18:30:00+00:00",
        "driver": None,
        "id": "039601aa-3608-419a-9b8d-b60fd8c80105",
        "max_bookings": 20,
        "route": {"id": "22f1ccd6-e7b8-4426-b67a-4c74009b8c80", "type": "route"},
        "start_time": "2020-04-13T05:30:00+00:00",
        "state": "PLANNED",
        "vehicle": {
            "id": "d824dbd6-3036-41f6-9d1e-25ea710b9d27",
            "registration_number": "30-3456",
        },
        "way_points": [
            {
                "departed_at": None,
                "estimated_departure_time": "2020-04-13T05:30:00+00:00",
                "id": "b92a30d4-8f61-45e5-8038-fb76c9c43541",
                "stop": {
                    "id": "e8d614eb-fd76-4ba5-b6ea-943a10b2fd5b",
                    "location": {"lat": 19.1176, "lng": 72.906},
                },
                "type": "PICKUP",
            },
            {
                "departed_at": None,
                "estimated_departure_time": "2020-04-13T05:31:00+00:00",
                "id": "4d44ea74-24d3-4e69-bf78-348e521b24e0",
                "stop": {
                    "id": "58ad12c1-12fb-49f7-9c32-11c2491ff7fa",
                    "location": {"lat": 19.1364, "lng": 72.8296},
                },
                "type": "DROP",
            },
        ],
    }


def booking_request_json() -> dict:
    return {
        "id": uuid4_str(),
        "user": {"id": uuid4_str(), "type": "user"},
        "modes": [{"type": "MANUAL", "id": uuid4_str()}],
        "created_at": "2020-04-13T05:30:00+00:00",
        "updated_at": "2020-04-13T05:30:00+00:00",
        "booking": {
            "pickup_stop": {"id": uuid4_str(), "type": "stop"},
            "drop_stop": {"id": uuid4_str(), "type": "stop"},
            "trip": {"id": uuid4_str(), "type": "trip"},
            "boarding_time": "2020-04-13T08:30:00+00:00",
            "status": "CONFIRMED",
            "cancellation_reason": None,
            "cancelled_at": None,
            "created_at": "2020-04-13T05:30:00+00:00",
            "updated_at": "2020-04-13T05:30:00+00:00",
            "boarding_info": None,
            "deboarding_info": None,
            "vehicle": {"id": uuid4_str(), "type": "vehicle"},
        },
        "missed_bookings_count": 0,
    }


def random_location() -> Location:
    lat = random.uniform(-90, 90)
    lng = random.uniform(-180, 180)
    return Location(lat, lng)


def test_from_dict_on_trip_json_from_api_v1():
    trip = Trip.from_dict(trip_json_from_v1_api())
    assert trip == trip1()


def test_from_dict_on_trip_json_from_api_v2():
    trip = Trip.from_dict(trip_json_from_v2_api())
    assert trip == trip2()


@responses.activate
def test_get_trips():
    route_id_1 = uuid4_str()
    route_id_2 = uuid4_str()
    time_window = TimeWindow()

    def request_callback(request: PreparedRequest) -> Tuple:
        assert route_id_1 in request.url
        assert route_id_2 in request.url
        return (
            200,
            {},
            json.dumps(
                {"data": [trip_json_from_v2_api()], "meta": {"cursor": {"last": None}}}
            ),
        )

    responses.add_callback(
        responses.GET, "http://dummy_b2c_tms/api/v2/trips", callback=request_callback,
    )

    b2c_tms_service.get_trips(
        route_ids=[route_id_1, route_id_2], time_window=time_window
    )


@responses.activate
def test_attach_vehicle_on_trip():
    trip = trip1()
    vehicle_id = trip.vehicle_id
    trip.vehicle = None

    def request_callback(request: PreparedRequest) -> Tuple:
        payload = json.loads(request.body)
        assert payload["id"] == vehicle_id
        return (
            200,
            {},
            json.dumps({"data": trip_json_from_v1_api()}),
        )

    responses.add_callback(
        responses.POST,
        f"http://dummy_b2c_tms/api/v1/trips/{trip.id}/vehicle",
        callback=request_callback,
        content_type="application/json",
    )

    b2c_tms_service.attach_vehicle_to_trip(trip_id=trip.id, vehicle_id=vehicle_id)


@responses.activate
def test_detach_vehicle_from_trip():
    trip = trip1()

    def request_callback(request: PreparedRequest) -> Tuple:
        assert not request.body
        return (
            200,
            {},
            json.dumps({"data": trip_json_from_v1_api()}),
        )

    responses.add_callback(
        responses.POST,
        f"http://dummy_b2c_tms/api/v1/trips/{trip.id}/vehicle/detach",
        callback=request_callback,
        content_type="application/json",
    )

    b2c_tms_service.detach_vehicle_from_trip(trip_id=trip.id)


@responses.activate
def test_update_vehicle_on_trip():
    trip = trip1()
    new_vehicle_id = uuid4_str()

    def request_callback(request: PreparedRequest) -> Tuple:
        payload = json.loads(request.body)
        assert payload == {
            "trip_id": trip.id,
            "from_vehicle_id": trip.vehicle_id,
            "to_vehicle_id": new_vehicle_id,
        }
        return (
            200,
            {},
            json.dumps({"data": trip_json_from_v1_api()}),
        )

    responses.add_callback(
        responses.POST,
        "http://dummy_b2c_tms/api/v1/trips/vehicle/update",
        callback=request_callback,
        content_type="application/json",
    )

    b2c_tms_service.update_vehicle_for_trip(
        trip_id=trip.id,
        current_vehicle_id=trip.vehicle_id,
        new_vehicle_id=new_vehicle_id,
    )


@responses.activate
def test_board():
    trip = trip1()
    time = time_now()
    location = random_location()
    mode = BoardingMode(type="MANUAL", id=uuid4_str())

    def request_callback(request: PreparedRequest) -> Tuple:
        payload = json.loads(request.body)
        assert payload == serialize(
            dict(trip_id=trip.id, time=time, location=location, mode=mode)
        )
        return (
            200,
            {},
            json.dumps({"data": booking_request_json()}),
        )

    responses.add_callback(
        responses.POST,
        "http://dummy_b2c_tms/api/v1/booking_requests/board",
        callback=request_callback,
        content_type="application/json",
    )

    b2c_tms_service.board(trip_id=trip.id, time=time, location=location, mode=mode)
