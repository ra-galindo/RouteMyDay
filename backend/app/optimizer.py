EXACT_THRESHOLD = 9    # Held-Karp for n ≤ this; heuristic above


# ── Held-Karp exact DP ────────────────────────────────────────────────────────

def _held_karp(dur_matrix, dist_matrix, fixed_start: bool, fixed_end: bool):
    """
    Exact open-path TSP via Held-Karp dynamic programming.
    Guaranteed optimal. O(2^n · n²).

    dp[mask][i] = minimum duration to have visited exactly the nodes in `mask`
                  and be standing at node i.
    """
    n = len(dur_matrix)
    INF = float("inf")
    size = 1 << n

    dp = [[INF] * n for _ in range(size)]
    parent = [[-1] * n for _ in range(size)]

    start = 0 if fixed_start else None
    end = n - 1 if fixed_end else None

    # Seed starting states
    if start is not None:
        dp[1 << start][start] = 0
    else:
        for s in range(n):
            if end is not None and s == end:
                continue          # don't allow the fixed end to also be the start
            dp[1 << s][s] = 0

    # Fill the table in order of increasing mask popcount
    for mask in range(1, size):
        for i in range(n):
            if dp[mask][i] == INF or not (mask >> i & 1):
                continue
            for j in range(n):
                if mask >> j & 1:
                    continue      # j already visited
                new_mask = mask | (1 << j)
                cost = dp[mask][i] + dur_matrix[i][j]
                if cost < dp[new_mask][j]:
                    dp[new_mask][j] = cost
                    parent[new_mask][j] = i

    all_mask = size - 1
    last = end if end is not None else min(range(n), key=lambda i: dp[all_mask][i])

    # Reconstruct path
    route, mask, curr = [], all_mask, last
    while curr != -1:
        route.append(curr)
        prev = parent[mask][curr]
        mask ^= (1 << curr)
        curr = prev
    route.reverse()

    total_dur = sum(dur_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))
    total_dist = sum(dist_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))
    return route, total_dist, total_dur


# ── Nearest-neighbour + 2-opt heuristic ──────────────────────────────────────

def _greedy_path(dist_matrix, dur_matrix, start: int, middle: set, end=None):
    route = [start]
    current = start
    total_dist = total_dur = 0
    remaining = set(middle)

    while remaining:
        nxt = min(remaining, key=lambda j: dur_matrix[current][j])
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


def _route_dur(route, dur_matrix):
    return sum(dur_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))


def _two_opt(route, dur_matrix, fixed_end: bool):
    """
    2-opt local search. Keeps route[0] fixed; keeps route[-1] fixed when fixed_end=True.
    """
    best = route[:]
    n = len(best)
    j_limit = n - 2 if fixed_end else n - 1
    improved = True

    while improved:
        improved = False
        for i in range(1, j_limit):
            for j in range(i + 1, j_limit + 1):
                candidate = best[:i] + best[i:j + 1][::-1] + best[j + 1:]
                if _route_dur(candidate, dur_matrix) < _route_dur(best, dur_matrix):
                    best = candidate
                    improved = True
                    break
            if improved:
                break

    return best


def _heuristic(dist_matrix, dur_matrix, fixed_start: bool, fixed_end: bool):
    """Nearest-neighbour seeding + 2-opt improvement."""
    n = len(dist_matrix)
    end_idx = (n - 1) if fixed_end else None
    free = set(range(n - 1 if fixed_end else n))

    if fixed_start:
        start_candidates = [0]
        free.discard(0)
    else:
        start_candidates = list(free)

    best_route, best_dist, best_dur = None, 0, float("inf")
    for s in start_candidates:
        middle = free - {s}
        route, dist, dur = _greedy_path(dist_matrix, dur_matrix, s, middle, end_idx)
        if dur < best_dur:
            best_route, best_dist, best_dur = route, dist, dur

    if len(best_route) > 3:
        best_route = _two_opt(best_route, dur_matrix, fixed_end)

    total_dist = sum(dist_matrix[best_route[i]][best_route[i + 1]] for i in range(len(best_route) - 1))
    total_dur = sum(dur_matrix[best_route[i]][best_route[i + 1]] for i in range(len(best_route) - 1))
    return best_route, total_dist, total_dur


# ── Public entry point ────────────────────────────────────────────────────────

def optimize_route(dist_matrix, dur_matrix, fixed_start: bool = False, fixed_end: bool = False):
    """
    Finds the fastest route through all stops.

    ≤ 9 stops  →  Held-Karp DP (exact, guaranteed optimal)
    > 9 stops  →  nearest-neighbour + 2-opt (fast heuristic, very good in practice)
    """
    n = len(dist_matrix)
    if n <= EXACT_THRESHOLD:
        return _held_karp(dur_matrix, dist_matrix, fixed_start, fixed_end)
    return _heuristic(dist_matrix, dur_matrix, fixed_start, fixed_end)