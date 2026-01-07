from pydantic import BaseModel
from typing import List, Optional

class Place(BaseModel):
    name: str
    lat: float
    lng: float

class OptimizeRequest(BaseModel):
    places: List[Place]
    fixed_end: bool = False

class OptimizeResponse(BaseModel):
    order: List[int]
    total_distance_km: float
