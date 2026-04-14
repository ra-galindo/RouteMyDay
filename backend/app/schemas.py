from typing import List
from pydantic import BaseModel


class OptimizeRequest(BaseModel):
    places: List[str]
    fixed_start: bool = False
    fixed_end: bool = False


class OptimizeResponse(BaseModel):
    order: List[int]
    total_distance_km: float
    total_duration_min: float