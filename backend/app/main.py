from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import OptimizeRequest, OptimizeResponse
from .maps import build_distance_matrix
from .optimizer import tsp_distance

app = FastAPI(title="RouteMyDay API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/optimize", response_model=OptimizeResponse)
def optimize(req: OptimizeRequest):
    matrix = build_distance_matrix(req.places)
    order, total_km = tsp_distance(matrix, req.fixed_end)

    return OptimizeResponse(
        order=order,
        total_distance_km=round(total_km, 2)
    )

@app.get("/ping")
def ping():
    return {"status": "ok"}
