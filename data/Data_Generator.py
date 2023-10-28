import copy
import random
import math


def create_costs(contributions, intervals):
    costs = [0] * len(intervals)
    eighty_percent_size = int(len(intervals) * 0.8)
    random_indexes = random.sample(range(len(intervals)), eighty_percent_size)
    random_indexes.sort()
    # print(random_indexes)
    max_costs = 0
    for i in random_indexes:
        number_of_tasks = intervals[i][1] - intervals[i][0] + 1
        costs[i] = random.randint(math.floor(contributions[i] * number_of_tasks / 3),
                                  contributions[i] * number_of_tasks)
        # print("Contribution of this i:",contributions[i])
        # print("Ceiling is:_______________________________________________________________________________________", contributions[i] * number_of_tasks)
        if contributions[i] * number_of_tasks > max_costs:
            max_costs = contributions[i] * number_of_tasks
    # print("max costs is: ", max_costs)
    # print(costs)
    for i in range(len(costs)):
        if costs[i] == 0:
            costs[i] = random.randint(1, max_costs)
    # print(costs)
    return costs


def task_one_contributions(intervals, contributions, demands, l1, while_counter=0):
    counter = -1
    max_contribution = 0
    for i in intervals:
        counter += 1
        if i[0] == 1:
            contributions[counter] = random.randint(1, math.ceil(4 * demands[0] / l1) + while_counter)
            max_contribution = max(contributions)
    return contributions, max_contribution


class DataGenerator:
    def __init__(self, num_tasks, seed=None):
        """
        :param num_tasks:
        :param seed:
        """
        self.num_tasks = num_tasks
        self.seed = seed

    def small_interval(self, task):
        if self.num_tasks == 10:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            # print("task is: ", task)
            # print("X is: ", x)
            # print("Y is: ", y)
        else:
            x = random.randint(0, 3)
            y = random.randint(0, 3)

        x = min(task - 1, x)
        y = min(self.num_tasks - task, y)

        result_list = [task - x, task + y]
        return result_list

    def create_demands(self):
        demands = []
        for _ in range(self.num_tasks):
            random_demand = random.randint(5, 20)
            demands.append(random_demand)
        return demands

    def run(self):

        random.seed(self.seed)
        intervals = []

        # SMALL WORKERS
        for _ in range(3 * self.num_tasks):
            random_task = random.randint(1, self.num_tasks)
            result = self.small_interval(random_task)
            intervals.append(result)

        print("Result array:", intervals)
        print("size is: ", len(intervals))

        # LARGE WORKERS
        large_workers = random.randint(0, math.ceil(3 * self.num_tasks / 20))
        print("number of large workers: ", large_workers)

        large_interval_map = {
            10: 5,
            20: 8,
            35: 10,
            50: 12,
            65: 14,
            75: 16,
            85: 18,
            100: 20,
        }

        if self.num_tasks in large_interval_map:
            large_interval = large_interval_map[self.num_tasks]
        else:
            large_interval = 0

        for _ in range(large_workers):
            random_task = random.randint(1, self.num_tasks)
            print("task now is:", random_task)
            if self.num_tasks == 10:  # large workers with 10 tasks
                start_interval = random_task - math.floor(large_interval / 2)
                end_interval = random_task + math.floor(large_interval / 2)
                if start_interval < 1:
                    carry = abs(start_interval) + 1
                    start_interval = 1
                    end_interval = end_interval + carry
                if end_interval > self.num_tasks:
                    carry = end_interval - self.num_tasks
                    end_interval = self.num_tasks
                    start_interval = start_interval - carry
            else:
                random_number = random.random()
                print("Chance is: ", random_number)
                if random_number < 0.5:
                    start_interval = int(random_task - (large_interval / 2))
                    end_interval = int(random_task + (large_interval / 2) - 1)
                    if start_interval < 1:
                        carry = abs(start_interval) + 1
                        start_interval = 1
                        end_interval = int(random_task + (large_interval / 2) - 1) + carry
                    elif end_interval > self.num_tasks:
                        carry = end_interval - self.num_tasks
                        end_interval = self.num_tasks
                        start_interval = int(random_task - (large_interval / 2)) - carry
                else:
                    start_interval = int(random_task - (large_interval / 2) + 1)
                    end_interval = int(random_task + (large_interval / 2))
                    if start_interval < 1:
                        carry = abs(start_interval) + 1
                        start_interval = 1
                        end_interval = int(random_task + (large_interval / 2)) + carry
                    elif end_interval > self.num_tasks:
                        carry = end_interval - self.num_tasks
                        end_interval = self.num_tasks
                        start_interval = int(random_task - (large_interval / 2) + 1) - carry
            intervals.append([start_interval, end_interval])

        for i in range(1, self.num_tasks + 1):  # check if task is uncovered, then add worker for it
            flag = False
            for j in intervals:
                if j[0] <= i <= j[1]:
                    flag = True
            if not flag:
                result = self.small_interval(i)
                intervals.append(result)

        print("Result array:", intervals)
        print("size is: ", len(intervals))

        # DEMANDS
        demands = self.create_demands()
        print("Demands: ", demands)

        # CONTRIBUTIONS
        while_counter = 0
        flag = True
        while flag:
            contributions = [0] * len(intervals)
            l1 = 0
            for i in intervals:
                if i[0] == 1:
                    l1 += 1
            print("λ1 is: ", l1)

            # task 1 contribution
            contributions, max_contribution = task_one_contributions(intervals, contributions, demands, l1, while_counter)
            # check if task 1 contribution is enough
            while sum(contributions) < demands[0]:
                contributions, max_contribution = task_one_contributions(intervals, contributions, demands, l1, while_counter)
            print("Contributions are", contributions)

            #first_task_contribution = copy.deepcopy(contributions)

            #contributions = copy.deepcopy(first_task_contribution)
            #print("--------------------------------", first_task_contribution)
            print("++++++++++++++++++++++++++++++++", contributions)
            # rest of the tasks contribution (self.num_tasks +1)
            for i in range(2, self.num_tasks + 1):
                Qj = 0
                # finding Qj
                first_counter = -1
                for j in contributions:
                    first_counter += 1
                    if j != 0:
                        if intervals[first_counter][0] <= i <= intervals[first_counter][1]:  # if task is covered
                            Qj += contributions[first_counter]
                # print("Qj: ", Qj)
                Qjnew = 2 * demands[i - 1] - Qj  # + math.random(-2, 2)
                # print("Qjnew", Qjnew)

                if Qjnew <= 0:
                    second_counter = -1
                    new_max = 0
                    task_covered = 0
                    # while task_covered < demands[i - 1]:
                    for j in contributions:
                        second_counter += 1
                        if j == 0:
                            if intervals[second_counter][0] <= i <= intervals[second_counter][1]:
                                if max_contribution < 1:
                                    max_contribution = 1
                                contributions[second_counter] = max(random.randint(1, max_contribution + while_counter), 1)
                                # print("contribution: ", contributions[second_counter])
                                task_covered += contributions[second_counter]
                                if contributions[second_counter] > new_max:
                                    new_max = contributions[second_counter]
                            # print("task_covered: ", task_covered)
                    # print("new_max is: ", new_max)
                    max_contribution = new_max
                    # print("New contributions: ", contributions)
                else:
                    ljnew = 0
                    third_counter = -1
                    # print("----", i)
                    for k in intervals:
                        third_counter += 1
                        # print("+++", k[0], contributions[third_counter])
                        if k[0] == i and contributions[third_counter] == 0:
                            ljnew += 1
                    # print("ljnew is: ", ljnew)
                    fourth_counter = -1
                    new_max = 0
                    for j in contributions:
                        fourth_counter += 1
                        if j == 0:
                            if intervals[fourth_counter][0] <= i <= intervals[fourth_counter][1]:
                                contributions[fourth_counter] = random.randint(1, math.ceil(2 * Qjnew / ljnew) +
                                                                               while_counter)
                                if contributions[fourth_counter] > new_max:
                                    new_max = contributions[fourth_counter]
                    # print("new_max is: ", new_max)
                    max_contribution = new_max
                    # print("New contributions: ", contributions)

            while_counter += 1
            # Check if all tasks meet their demands
            all_tasks_met_demands = True
            for i in range(2, self.num_tasks + 1):
                counter = -1
                current_task_contribution = 0
                for k in contributions:
                    counter += 1
                    if intervals[counter][0] <= i <= intervals[counter][1]:
                        current_task_contribution += k
                if current_task_contribution < demands[i - 1]:
                    print(current_task_contribution, demands[i - 1])
                    print(demands)
                    all_tasks_met_demands = False
                    break
            print("Contributions: ", contributions)
            # If all tasks meet their demands, exit the loop
            if all_tasks_met_demands:
                flag = False
                break

            """
            counter = -1
            current_task_contribution = 0
            for k in contributions:
                counter += 1
                if k != 0:
                    if intervals[counter][0] <= i <= intervals[counter][1]:
                        current_task_contribution += k
            print("current_task_contribution: ", current_task_contribution)

            if current_task_contribution <= demands[i - 1]:
                print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            print("Contributions: ", contributions)
            """
        # COSTS
        costs = create_costs(contributions, intervals)
        print("Costs: ", costs)
        print(" ")
        print("----------------------")

        return intervals, demands, contributions, costs


"""
num_tasks = 10
seed = 42
data_generator = DataGenerator(num_tasks, seed)
data_generator.run()
"""
