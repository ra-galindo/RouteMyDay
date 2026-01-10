from fastapi import FastAPI, HTTPException
from .schemas import OptimizeRequest, OptimizeResponse
from .optimizer import optimize_route
from .maps import get_distance_matrix

app = FastAPI(title="RouteMyDay API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/optimize", response_model=OptimizeResponse)
async def optimize(request: OptimizeRequest):
    places = request.places

    if len(places) < 2:
        raise HTTPException(status_code=400, detail="At least two places are required")

    # get distance matrix via Google Maps
    distance_matrix = await get_distance_matrix(places)

    # optimize route
    order, total_distance = optimize_route(distance_matrix, round_trip=request.round_trip)

    return OptimizeResponse(
        order=order,
        total_distance_km=round(total_distance / 1000, 2)
    )
