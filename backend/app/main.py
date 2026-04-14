from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import OptimizeRequest, OptimizeResponse
from .optimizer import optimize_route
from .maps import get_distance_matrix

app = FastAPI(title="RouteMyDay API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/optimize", response_model=OptimizeResponse)
async def optimize(request: OptimizeRequest):
    if len(request.places) < 2:
        raise HTTPException(status_code=400, detail="At least two places are required.")

    dist_matrix, dur_matrix = await get_distance_matrix(request.places)

    order, total_dist, total_dur = optimize_route(
        dist_matrix,
        dur_matrix,
        fixed_start=request.fixed_start,
        fixed_end=request.fixed_end,
    )

    return OptimizeResponse(
        order=order,
        total_distance_km=round(total_dist / 1000, 2),
        total_duration_min=round(total_dur / 60, 1),
    )