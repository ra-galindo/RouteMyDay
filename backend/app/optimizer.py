from typing import List
import math

def tsp_distance(matrix: List[List[float]], fixed_end: bool):

    n = len(matrix)
    dp = {}
    parent = {}

    for i in range(1, n):
        dp[(1 << i, i)] = matrix[0][i]

    for mask in range(1 << n):
        for j in range(n):
            if not (mask & (1 << j)):
                continue

            prev_mask = mask ^ (1 << j)

            if prev_mask == 0:
                continue

            for k in range(n):
                if not (prev_mask & (1 << k)):
                    continue

                prev = dp.get((prev_mask, k), math.inf)
                cand = prev + matrix[k][j]

                if cand < dp.get((mask, j), math.inf):
                    dp[(mask, j)] = cand
                    parent[(mask, j)] = k

    full_mask = (1 << n) - 1

    best_cost = math.inf
    end_node = None

    for j in range(1, n):
        cost = dp[(full_mask, j)]
        if not fixed_end:
            cost += matrix[j][0]

        if cost < best_cost:
            best_cost = cost
            end_node = j

    order = [0]
    mask = full_mask
    j = end_node

    while j != 0:
        order.append(j)
        pj = parent[(mask, j)]
        mask ^= 1 << j
        j = pj

    order.append(0 if not fixed_end else end_node)
    order.reverse()

    return order, best_cost / 1000.0
