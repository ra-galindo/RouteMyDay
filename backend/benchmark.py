"""
Run from the backend folder:
    python benchmark.py

Benchmarks Held-Karp across different stop counts using random distance/duration
matrices so you can see the actual runtime without hitting the Google Maps API.
"""

import random
import time
from app.optimizer import optimize_route

random.seed(42)

def random_matrix(n, lo=60, hi=1800):
    """Random symmetric-ish duration matrix (seconds), zeroes on diagonal."""
    m = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                m[i][j] = random.randint(lo, hi)
    return m

print(f"{'Stops':>6}  {'Algorithm':>20}  {'Time':>10}")
print("-" * 44)

for n in range(2, 16):
    dur = random_matrix(n)
    dist = random_matrix(n, 500, 10000)

    start = time.perf_counter()
    optimize_route(dist, dur, fixed_start=False, fixed_end=False)
    elapsed = time.perf_counter() - start

    algo = "Held-Karp (exact)" if n <= 12 else "NN + 2-opt (heuristic)"
    print(f"{n:>6}  {algo:>20}  {elapsed * 1000:>8.1f} ms")