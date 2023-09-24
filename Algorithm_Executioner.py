import pandas as pd
import xlsxwriter
import argparse

from algorithms.LMIS_deletion import A
from algorithms.LMIS_included import Algo
from algorithms.IntegerProgram import IP
import ast
import os
import csv

experimental_results = []


def save_results(cost, del_cos, opt_cost, path_name, file_name, num_workers, num_tasks):
    experimental_results.append(
        {'dataset': path_name, 'instance': file_name, 'num_workers': num_workers, 'num_tasks': num_tasks,
         'algorithm_cost': cost, 'deletion_cost': del_cos, 'optimal_cost': opt_cost})

    if len(experimental_results) % 10 == 0:
        results_path_name = 'results_for_' + path_name

        fieldnames = ['dataset', 'instance', 'num_workers', 'num_tasks', 'algorithm_cost', 'deletion_cost',
                      'optimal_cost']

        if not results_path_name.endswith('.xlsx'):
            results_path_name += '.xlsx'

        save_path = 'results'
        full_file_path = os.path.join(save_path, results_path_name)
        workbook = xlsxwriter.Workbook(full_file_path)
        worksheet = workbook.add_worksheet()
        bold_format = workbook.add_format({'bold': True})

        for col_num, field in enumerate(fieldnames):
            worksheet.write(0, col_num, field, bold_format)

        for row_num, result in enumerate(experimental_results):
            for col_num, field in enumerate(fieldnames):
                worksheet.write(row_num + 1, col_num, result[field])

        workbook.close()

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


class AlgorithmExecutioner:

    def __init__(self, bidding_profile, contribution, demand):
        self.P1 = Algo(bidding_profile, contribution, demand)
        self.P2 = A(bidding_profile, contribution, demand)
        self.P3 = IP(bidding_profile, contribution, demand)

    def run(self, path_name, file_name):
        num_workers = int(path_name.split('_')[0].split('workers')[0])
        num_tasks = int(path_name.split('_')[2].split('tasks')[0])

        sol, cost = self.P1.run()
        order, final_sol, final_cos = self.P2.run()
        opt_values, opt_cost = self.P3.solve()
        print("---------- Solution for instance: ", file_name, "----------")
        if sol != 0 and cost != 0:
            print("LMIS solution is:", sol)
            print("The cost is:", cost)
            print("Order of selection is:", order)
            print("LMIS solution after deletion is:", final_sol)
            print("The final cost after deletion is:", final_cos)
        else:
            print("Infeasible Solution for this instance")

        for i in range(len(opt_values)):
            if opt_values[i] > 0:
                opt_values[i] = i + 1

        opt_values = [i for i in opt_values if i != 0]

        if opt_values is not None and opt_cost is not None:
            print("Optimal selection is:", opt_values)
            print("Optimal cost:", opt_cost)

        save_results(cost, final_cos, opt_cost, path_name, file_name, num_workers, num_tasks)


parser = argparse.ArgumentParser(description='Algorithm Execution')
parser.add_argument('--path_name', type=str, help='Path name')
args = parser.parse_args()

if __name__ == '__main__':
    filenames = ['instance01.csv', 'instance02.csv', 'instance03.csv', 'instance04.csv', 'instance05.csv',
                 'instance06.csv', 'instance07.csv', 'instance08.csv', 'instance09.csv', 'instance10.csv']
    path_name = args.path_name
    for filename in filenames:
        dataset_path = os.path.join(os.path.dirname(__file__), 'datasets\\' + path_name, filename)
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
                    q.append(int(row['contribution']))
            file.seek(0)  # reset file pointer
            next(reader)

            for row in reader:
                if row['demand'] != '':
                    d.append(int(row['demand']))

        main_program = AlgorithmExecutioner(b, q, d)
        main_program.run(path_name, filename)
