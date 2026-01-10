from typing import List
from pydantic import BaseModel


class OptimizeRequest(BaseModel):
    places: List[str]
    round_trip: bool = False


class OptimizeResponse(BaseModel):
    order: List[int]
    total_distance_km: float
