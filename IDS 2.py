import math
from itertools import permutations

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def total_distance(route):
    distance = 0
    for i in range(1, len(route)):
        distance += euclidean_distance(route[i-1], route[i])
    return distance

def optimize_route(locations, priorities):
    deliveries = [(locations[i], priorities[i]) for i in range(len(locations))]

    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    deliveries.sort(key=lambda x: priority_order[x[1]])

    sorted_locations = [delivery[0] for delivery in deliveries]

    min_distance = float('inf')
    best_route = None
    for perm in permutations(sorted_locations):
        dist = total_distance(perm)
        if dist < min_distance:
            min_distance = dist
            best_route = perm
    
    return best_route, min_distance

def main():
    locations_input = input("Enter locations as a list of tuples (e.g., [(0, 0), (2, 3), (5, 1)]): ")
    priorities_input = input("Enter priorities as a list (e.g., ['high', 'medium', 'low']): ")

    locations = eval(locations_input)
    priorities = eval(priorities_input)

    optimized_route, total_dist = optimize_route(locations, priorities)

    print(f"Optimized Route: {optimized_route}")
    print(f"Total Distance: {total_dist:.2f} units")

if __name__ == "__main__":
    main()
