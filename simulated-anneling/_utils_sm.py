import contextlib
import json
import random
import numpy as np

def __from_matrix_to_json_file(matrix, file_path):
    json_data = {}
    for i in range(len(matrix)):
        json_data[str(i + 1)] = {}
        for j in range(len(matrix)):
            json_data[str(i + 1)][str(j + 1)] = matrix[i][j]

    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file)


def load_distances(json_path: str):
    with open(json_path, "r") as f:
        data = json.load(f)
        with contextlib.suppress(Exception):
            data = {int(key): {int(key2): value2 for key2, value2 in value.items()}
                    for key, value in data.items()}
    return data


def create_random_number(iteration_number):
    return [round(random.random(), 2) for _ in range(iteration_number)]


def compare_solution(solution1, solution2):
    return solution1 == solution2


def temperature(beta, tk):
    return round((beta * tk), 2)


def calculate_distance(data_matrix, solution):
    return sum(data_matrix.get(solution[i]).get(solution[i + 1]) for i in range(len(solution) - 1))


def move_cities(solution_list):
    random_list = random.sample(solution_list[1:-1], 2)
    city1, city2 = random_list[0], random_list[1]
    solution_list[solution_list.index(city1)], solution_list[solution_list.index(city2)] = city2, city1
    return solution_list


def _calculate_probabilty(current,candidate,temperature):
    return round(np.exp((candidate - current)/temperature),3)


distances = load_distances('five_city.json')
# initial_solution = [1, 2, 3, 4, 5, 1]
# print(distances)
# # print(calculate_distance(distances, initial_solution))
# # print(temperature(0.4, calculate_distance(distances, initial_solution)))
# for _ in range(3):
#     print(move_cities(initial_solution))
# #
# print(distances)