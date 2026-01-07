import os
import requests
from typing import List
from .schemas import Place

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def build_distance_matrix(places: List[Place]):
    origins = "|".join([f"{p.lat},{p.lng}" for p in places])
    destinations = origins

    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origins}&destinations={destinations}"
        f"&mode=walking&key={GOOGLE_API_KEY}"
    )

    res = requests.get(url)
    data = res.json()

    matrix = []
    for row in data["rows"]:
        matrix.append([elem["distance"]["value"] for elem in row["elements"]])

    return matrix  # meters
