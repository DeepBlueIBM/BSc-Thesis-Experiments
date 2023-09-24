import argparse
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class Visualizer:
    def __init__(self, path_name):
        self.grouped_data = None
        self.data = pd.read_excel('results\\' + path_name + '.xlsx')
        print(self.data.describe())  # pandas built-in analysis

    def plot_average_cost_by_group(self):
        self.grouped_data = self.data.groupby(['num_workers', 'num_tasks']).agg({
            'algorithm_cost': 'mean',
            'deletion_cost': 'mean',
            'optimal_cost': 'mean'
        }).reset_index()
        print(self.grouped_data)

        plt.figure(figsize=(8, 6))
        bar_width = 0.2
        space = 0.1
        index = np.arange(len(self.grouped_data))

        plt.bar(index, self.grouped_data['algorithm_cost'], width=bar_width, label='Algorithm Cost')
        plt.bar(index + bar_width + space, self.grouped_data['deletion_cost'], width=bar_width, label='Deletion Cost')
        plt.bar(index + 2 * (bar_width + space), self.grouped_data['optimal_cost'], width=bar_width, label='Optimal Cost')

        plt.xticks(index + bar_width + space, self.grouped_data['num_workers'].astype(str) + ' workers, ' +
                   self.grouped_data['num_tasks'].astype(str) + ' tasks', rotation=0)
        plt.xlabel('Group')
        plt.ylabel('Average Cost')
        plt.title('Average Cost by Group')
        plt.legend()

        plt.show()

    def plot_cost_for_individual_instances(self):
        plt.figure(figsize=(10, 6))
        bar_width = 0.2
        index = np.arange(len(self.data))

        algorithm_cost = self.data['algorithm_cost']
        deletion_cost = self.data['deletion_cost']
        optimal_cost = self.data['optimal_cost']

        plt.bar(index, algorithm_cost, width=bar_width, label='Algorithm Cost')
        plt.bar(index + bar_width, deletion_cost, width=bar_width, label='Deletion Cost')
        plt.bar(index + 2 * bar_width, optimal_cost, width=bar_width, label='Optimal Cost')

        x_labels = ['instance{:02d}'.format(i + 1) for i in range(len(self.data))]
        plt.xticks(index + bar_width, x_labels, rotation=25, ha='right')

        plt.xlabel('Instances')
        plt.ylabel('Cost')
        plt.title('Cost for Individual Instances')
        plt.legend()

        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Algorithm Execution')
    parser.add_argument('--path_name', type=str, help='Path name')
    parser.add_argument('--plot_type', type=str, help='Plot type: group or individual')
    args = parser.parse_args()

    path_name = args.path_name
    visual = Visualizer(path_name)

    if args.plot_type == 'group':
        visual.plot_average_cost_by_group()
    elif args.plot_type == 'individual':
        visual.plot_cost_for_individual_instances()
    else:
        print("Invalid plot type. Choose either 'group' or 'individual'.")
