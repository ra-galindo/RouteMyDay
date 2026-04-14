import os
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

if not API_KEY:
    raise RuntimeError("GOOGLE_MAPS_API_KEY environment variable must be set in .env")


async def get_distance_matrix(places: list[str]):
    """
    Returns (dist_matrix, dur_matrix) where values are in metres and seconds.
    """
    params = {
        "origins": "|".join(places),
        "destinations": "|".join(places),
        "key": API_KEY,
        "units": "metric",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(
            "https://maps.googleapis.com/maps/api/distancematrix/json",
            params=params,
        )

    data = resp.json()

    if data.get("status") != "OK":
        raise HTTPException(
            status_code=500,
            detail=f"Google Maps API error: {data.get('status')} — {data.get('error_message', '')}",
        )

    dist_matrix, dur_matrix = [], []

    for i, row in enumerate(data["rows"]):
        row_dists, row_durs = [], []
        for j, elem in enumerate(row["elements"]):
            if elem.get("status") != "OK":
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Could not calculate route from '{places[i]}' to "
                        f"'{places[j]}': {elem.get('status')}"
                    ),
                )
            row_dists.append(elem["distance"]["value"])   # metres
            row_durs.append(elem["duration"]["value"])    # seconds
        dist_matrix.append(row_dists)
        dur_matrix.append(row_durs)

    return dist_matrix, dur_matrix