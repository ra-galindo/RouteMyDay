def optimize_route(distance_matrix, round_trip: bool = False):
    n = len(distance_matrix)
    unvisited = set(range(1, n))
    route = [0]
    total_distance = 0

    current = 0

    while unvisited:
        next_city = min(
            unvisited,
            key=lambda j: distance_matrix[current][j]
        )
        total_distance += distance_matrix[current][next_city]
        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    if round_trip:
        total_distance += distance_matrix[current][0]
        route.append(0)

    return route, total_distance
