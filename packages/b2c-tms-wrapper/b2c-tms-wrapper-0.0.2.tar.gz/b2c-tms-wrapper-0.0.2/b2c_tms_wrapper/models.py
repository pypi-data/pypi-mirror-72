from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List

from shuttlis.geography import Location


class TripState(Enum):
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class Vehicle:
    id: str
    registration_number: str

    @classmethod
    def from_dict(cls, dikt: dict) -> "Vehicle":
        return cls(id=dikt["id"], registration_number=dikt.get("registration_number"))


@dataclass
class Stop:
    id: str
    location: Optional[Location] = None

    @classmethod
    def from_dict(self, dikt: dict) -> "Stop":
        return Stop(
            id=dikt["id"],
            location=Location(**dikt["location"]) if dikt.get("location") else None,
        )


@dataclass
class TripTrackedWayPoint:
    id: str
    stop: Stop
    estimated_departure_time: datetime
    departed_at: Optional[datetime]

    @classmethod
    def from_dict(self, dikt: dict) -> "TripTrackedWayPoint":
        return TripTrackedWayPoint(
            id=dikt["id"],
            stop=Stop.from_dict(dikt["stop"]),
            estimated_departure_time=datetime.fromisoformat(
                dikt["estimated_departure_time"]
            )
            if dikt.get("estimated_departure_time")
            else datetime.fromisoformat(dikt["departure_time"])
            if dikt.get("departure_time")
            else None,
            departed_at=datetime.fromisoformat(dikt["departed_at"])
            if dikt.get("departed_at")
            else None,
        )


@dataclass
class Trip:
    id: str
    route_id: str
    start_time: datetime
    state: TripState
    max_bookings: int
    vehicle: Optional[Vehicle]
    way_points: List[TripTrackedWayPoint]

    @classmethod
    def from_dict(cls, dikt: dict) -> "Trip":
        return cls(
            id=dikt["id"],
            route_id=dikt["route"]["id"],
            state=TripState(dikt["state"]),
            start_time=datetime.fromisoformat(dikt["start_time"]),
            max_bookings=int(dikt["max_bookings"]),
            vehicle=Vehicle.from_dict(dikt["vehicle"]) if dikt["vehicle"] else None,
            way_points=[
                TripTrackedWayPoint.from_dict(way_point)
                for way_point in dikt["way_points"]
            ],
        )

    @property
    def departure_time_for_first_stop(self) -> datetime:
        return self.way_points[0].estimated_departure_time

    @property
    def vehicle_id(self) -> str:
        return self.vehicle.id if self.vehicle else None


@dataclass
class BookingRequest:
    id: str
    trip_id: str
    boarding_info: Optional[dict]

    @classmethod
    def from_dict(cls, dikt: dict) -> "BookingRequest":
        return BookingRequest(
            id=dikt["id"],
            trip_id=dikt["booking"]["trip"]["id"],
            boarding_info=dikt["booking"]["boarding_info"],
        )

    @property
    def is_boarded(self) -> bool:
        return bool(self.boarding_info)


@dataclass
class BoardingMode:
    type: str
    id: str
