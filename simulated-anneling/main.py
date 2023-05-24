import json
import _utils_sm
import matplotlib.pyplot as plt

class SimulatedAnneling():
    def __init__(self, json_path: str, iteration_number: int):
        self.data = _utils_sm.load_distances(json_path)
        self.iteration_number = iteration_number
        self.first_iteration = 1
        self.Uk = _utils_sm.create_random_number(self.iteration_number)
        self.T1 = 0
        self.tk = 0
        self.initial_solution = [1,2,3,4,5,6,7,8,9,10,1]
        self.distances = _utils_sm.load_distances(json_path)
        self.best_path=[]
        self.candidate_path = []
        self.sk_path = []
        self.best_of=0
        self.candidate_of =0
        self.sk_of = 0
        self.best_of_list = []
        self.candidate_of_list = []
        self.sk_of_list = []
    def get_distances(self):
        return self.distances
    def get_calculated_distance(self,solution):
        return _utils_sm.calculate_distance(self.distances,solution)
    def run_iterations(self):
        while self.first_iteration <= self.iteration_number:
            if self.first_iteration ==1:
                print("First Iteration")
                print("-----------------")
                self.best_path = self.initial_solution
                self.sk_path = self.initial_solution
                print("Best Path : ", self.best_path)
                print("Sk path:", self.sk_path)

                self.best_of = self.get_calculated_distance(self.best_path)
                self.best_of_list.append(self.best_of)
                self.sk_of = self.get_calculated_distance(self.sk_path)
                self.sk_of_list.append(self.sk_of)
                # self.best_of_list.append(self.best_of)
                self.T1 = _utils_sm.temperature(0.6,self.best_of)
                print("Best path value:", self.best_of)
                print("T1 value:", self.T1)
                self.candidate_path = self.change_candidate_path(self.initial_solution)
                while True:
                    if _utils_sm.compare_solution(self.candidate_path, self.initial_solution):
                        self.candidate_path = self.change_candidate_path(self.initial_solution)
                    break

                self.candidate_of = self.get_calculated_distance(self.candidate_path)
                self.candidate_of_list.append(self.candidate_of)
                print("Candidate path:", self.candidate_path)
                print("Candidate path value:", self.candidate_of)


                if self.best_of >= self.candidate_of:
                    self.sk_path = self.candidate_path
                    self.best_path = self.candidate_path
                    self.best_of = self.candidate_of
                    self.best_of_list.append(self.best_of)

                if self.best_of < self.candidate_of:
                    if self.Uk[0] <= _utils_sm._calculate_probabilty(self.best_of,self.candidate_of,self.T1):
                        self.sk_path = self.candidate_path
                    else:
                        self.sk_path = self.sk_path
                self.first_iteration+=1
            else:
                print("iteration number : ", self.first_iteration)
                print("---------------")
                self.sk_of = self.get_calculated_distance(self.sk_path)
                self.sk_of_list.append(self.sk_of)
                self.tk = _utils_sm.temperature(0.5,self.sk_of)
                print("Sk path:", self.sk_path)
                print("tk value:", self.tk)

                self.candidate_path = self.change_candidate_path(self.sk_path)
                while True:
                    if _utils_sm.compare_solution(self.candidate_path,self.sk_path):
                        self.candidate_path = self.change_candidate_path(self.sk_path)
                    break
                self.candidate_of = self.get_calculated_distance(self.candidate_path)
                self.candidate_of_list.append(self.candidate_of)
                print("Candidate path:", self.candidate_path)
                print("Candidate path value:", self.candidate_of)

                if self.best_of<self.candidate_of and self.candidate_of<self.sk_of:
                    self.sk_path = self.candidate_path

                if self.candidate_of < self.best_of:
                    self.best_path = self.candidate_path
                    self.sk_path = self.candidate_path
                    self.best_of = self.candidate_of

                if self.candidate_of > self.best_of:
                    if self.Uk[self.iteration_number-1] <=_utils_sm._calculate_probabilty(self.best_of,self.candidate_of,self.tk):
                        print("probability:",_utils_sm._calculate_probabilty(self.best_of,self.candidate_of,self.tk))
                        self.sk_path = self.candidate_path
                    else:
                        self.sk_path = self.sk_path
                self.first_iteration+=1
                self.best_of_list.append(self.best_of)

        print("Best of list",self.best_of_list)
        print("Candidate of list:", self.candidate_of_list)
        print(len(self.best_of_list))
        print(len(self.candidate_of_list))
        print("Sk list:",self.sk_of_list)
        print("Best path:",self.best_path)
        # self._show_graphs(self.best_of_list, self.candidate_of_list, self.iteration_number)
        self._show_graphs(self.best_of_list, self.sk_of_list, self.iteration_number)

    def change_candidate_path(self,change_path):
        return _utils_sm.move_cities(change_path)

    def _show_graphs(self,objfunctbest, objfunctcandidate,iteration_number):
        x_axis = list(_ for _ in range(1,iteration_number+1))
        y1 = objfunctbest[:-1]
        y2 = objfunctcandidate
        plt.title("Number of cities: 10 iteration number: 150")
        plt.plot(x_axis,y1,label='Sbest values')
        plt.plot(x_axis,y2, label='Sk values')
        plt.legend(bbox_to_anchor =(0.65, 1.25))
        plt.show()


sa = SimulatedAnneling(json_path='ten_city.json',iteration_number=150)
print(sa.get_distances())
print("-----------")
print(sa.Uk)
initial_solution = [1, 2, 3, 4, 5,6,7,8,9,10,1]
sa.run_iterations()
