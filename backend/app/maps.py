import os
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()



API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

print(">>> GOOGLE_MAPS_API_KEY:", API_KEY)


if not API_KEY:
    raise RuntimeError("GOOGLE_MAPS_API_KEY environment variable must be set in .env")


async def get_distance_matrix(places: list[str]):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    origins = "|".join(places)
    destinations = "|".join(places)

    params = {
        "origins": origins,
        "destinations": destinations,
        "key": API_KEY,
        "units": "metric"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, params=params)

    data = resp.json()

    if data.get("status") != "OK":
        raise HTTPException(status_code=500, detail=f"Google Maps API error: {data.get('status')}")

    matrix = []
    for row in data["rows"]:
        matrix.append([elem["distance"]["value"] for elem in row["elements"]])

    return matrix
