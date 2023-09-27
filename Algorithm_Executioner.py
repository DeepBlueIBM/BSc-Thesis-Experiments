# -- pathname x_tasks
import pandas as pd
import argparse
import time

from algorithms.LMIS_deletion import A
from algorithms.LMIS_included import Algo
from algorithms.IntegerProgram import IP
import ast
import os
import csv

start_time = time.time()

experimental_results = []


def save_results_to_csv(cost, del_cos, opt_cost, path_name, file_name, num_workers, num_tasks, delta, max_delta_index,
                        alg_set, opt_set, del_set):
    experimental_results.append(
        {'dataset': path_name, 'instance': file_name, 'num_workers': num_workers, 'num_tasks': num_tasks,
         'delta': delta, 'max_delta_index': max_delta_index, 'algorithm_solution_set': alg_set,
         'deletion_solution_set': del_set, 'optimal_solution_set': opt_set,
         'algorithm_cost': cost, 'deletion_cost': del_cos, 'optimal_cost': opt_cost})

    if len(experimental_results) % 20 == 0:
        results_path_name = 'results_for_' + path_name

        if not results_path_name.endswith('.csv'):
            results_path_name += '.csv'

        save_path = 'results'
        full_file_path = os.path.join(save_path, results_path_name)

        fieldnames = ['dataset', 'instance', 'num_workers', 'num_tasks', 'delta', 'max_delta_index',
                      'algorithm_solution_set', 'deletion_solution_set', 'optimal_solution_set', 'algorithm_cost',
                      'deletion_cost', 'optimal_cost']

        with open(full_file_path, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()  # Write the header row

            for result in experimental_results:
                writer.writerow(result)

        print("Results saved to:", full_file_path)
        """
        data = pd.DataFrame(experimental_results)
        grouped_data = data.groupby(['num_workers', 'num_tasks']).agg({
            'algorithm_cost': 'mean',
            'deletion_cost': 'mean',
            'optimal_cost': 'mean'
        }).reset_index()

        grouped_data.insert(0, 'dataset', path_name)

        results_path = os.path.join('results', 'summed_results.xlsx')
        if os.path.isfile(results_path):
            existing_data = pd.read_excel(results_path)
        else:
            existing_data = pd.DataFrame()

        merged_data = pd.concat([existing_data, grouped_data]).drop_duplicates()

        merged_data.to_excel(results_path, index=False)
        print(merged_data)
        """


class AlgorithmExecutioner:

    def __init__(self, bidding_profile, contribution, demand):
        self.P1 = Algo(bidding_profile, contribution, demand)
        self.P2 = A(bidding_profile, contribution, demand)
        self.P3 = IP(bidding_profile, contribution, demand)

    def run(self, path_name, file_name):
        num_tasks = int(path_name.split('_')[0].split('tasks')[0])
        #num_workers = 41

        sol, cost = self.P1.run()
        if sol != 0 and cost != 0:
            order, final_sol, final_cos, delta, max_delta_index, num_workers = self.P2.run()
            opt_values, opt_cost = self.P3.solve()
            print("---------- Solution for instance: ", file_name, "----------")
            print("LMIS solution is:", sol)
            print("The cost is:", cost)
            print("Order of selection is:", order)
            print("LMIS solution after deletion is:", final_sol)
            print("The final cost after deletion is:", final_cos)
            print("Δ is:", delta)
            print("Max Δ task is:", max_delta_index)

            for i in range(len(opt_values)):
                if opt_values[i] > 0:
                    opt_values[i] = i + 1

            opt_values = [i for i in opt_values if i != 0]

            if opt_values is not None and opt_cost is not None:
                print("Optimal selection is:", opt_values)
                print("Optimal cost:", opt_cost)
        else:
            print("Infeasible Solution for instance: ", file_name)
            final_cos, opt_cost, delta, max_delta_index, final_sol, opt_values, num_workers = 0, 0, 0, 0, 0, 0, 0

        # print("++++++++++++++++++++++++++++++++++++++++++", num_workers)
        save_results_to_csv(cost, final_cos, opt_cost, path_name, file_name, num_workers, num_tasks,
                            delta, max_delta_index, sol, opt_values, final_sol)


parser = argparse.ArgumentParser(description='Algorithm Execution')
parser.add_argument('--path_name', type=str, help='Path name')
args = parser.parse_args()

if __name__ == '__main__':
    filenames = ['instance01.csv', 'instance02.csv', 'instance03.csv', 'instance04.csv', 'instance05.csv',
                 'instance06.csv', 'instance07.csv', 'instance08.csv', 'instance09.csv', 'instance10.csv',
                 'instance11.csv', 'instance12.csv', 'instance13.csv', 'instance14.csv', 'instance15.csv',
                 'instance16.csv', 'instance17.csv', 'instance18.csv', 'instance19.csv', 'instance20.csv']
    path_name = args.path_name
    for filename in filenames:
        dataset_path = os.path.join(os.path.dirname(__file__), 'data\\', path_name,
                                    filename)  # 'data\\' + path_name, filename
        with open(dataset_path) as file:
            reader = csv.DictReader(file)
            b = []
            q = []
            d = []

            for row in reader:
                if row['bidding_profile'] != '':
                    b.append(ast.literal_eval(row['bidding_profile']))
            file.seek(0)  # reset file pointer
            next(reader)

            for row in reader:
                if row['contribution'] != '':
                    q.append(float(row['contribution']))
            file.seek(0)  # reset file pointer
            next(reader)

            for row in reader:
                if row['demand'] != '':
                    d.append(int(row['demand']))

        main_program = AlgorithmExecutioner(b, q, d)
        main_program.run(path_name, filename)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
