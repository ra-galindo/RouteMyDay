def _greedy_path(dist_matrix, dur_matrix, start: int, middle: set, end=None):
    """
    Nearest-neighbour through `middle` stops starting from `start`,
    optionally ending at a fixed `end` index.
    Returns (route, total_distance_m, total_duration_s).
    """
    route = [start]
    current = start
    total_dist = 0
    total_dur = 0
    remaining = set(middle)

    while remaining:
        nxt = min(remaining, key=lambda j: dist_matrix[current][j])
        total_dist += dist_matrix[current][nxt]
        total_dur += dur_matrix[current][nxt]
        route.append(nxt)
        remaining.remove(nxt)
        current = nxt

    if end is not None:
        total_dist += dist_matrix[current][end]
        total_dur += dur_matrix[current][end]
        route.append(end)

    return route, total_dist, total_dur


def optimize_route(dist_matrix, dur_matrix, fixed_start: bool = False, fixed_end: bool = False):
    """
    Finds the shortest route through all stops using nearest-neighbour heuristic.

    fixed_start — first place in the list is always the starting point
    fixed_end   — last place in the list is always the ending point

    Returns (order, total_distance_m, total_duration_s).
    """
    n = len(dist_matrix)

    end_idx = (n - 1) if fixed_end else None

    # All indices that can serve as start or middle stops (excludes fixed end)
    free = set(range(n - 1 if fixed_end else n))

    if fixed_start:
        start_candidates = [0]
        free.discard(0)   # 0 is the start, not part of middle
    else:
        start_candidates = list(free)

    best_route, best_dist, best_dur = None, float("inf"), 0

    for s in start_candidates:
        middle = free - {s}
        route, dist, dur = _greedy_path(dist_matrix, dur_matrix, s, middle, end_idx)
        if dist < best_dist:
            best_route, best_dist, best_dur = route, dist, dur

    return best_route, best_dist, best_dur