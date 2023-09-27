import csv
import os
import matplotlib.pyplot as plt


class GraphPlot:

    def __init__(self):
        self.average_task_ratios = []
        self.worst_task_ratios = []
        self.average_deletion_ratios = []
        self.worst_deletion_ratios = []

    def read_costs_from_csv(self, file_path):
        algorithm_costs = []
        deletion_costs = []
        optimal_costs = []

        try:
            with open(file_path, mode='r', newline='') as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    algorithm_cost = float(row['algorithm_cost'])
                    deletion_cost = float(row['deletion_cost'])
                    optimal_cost = float(row['optimal_cost'])

                    algorithm_costs.append(algorithm_cost)
                    deletion_costs.append(deletion_cost)
                    optimal_costs.append(optimal_cost)

        except FileNotFoundError:
            print(f"File not found: {file_path}")

        return algorithm_costs, deletion_costs, optimal_costs

    def calculate_data(self, algorithm_costs, deletion_costs, optimal_costs):
        task_ratios = [algo_cost / opt_cost for algo_cost, opt_cost in zip(algorithm_costs, optimal_costs)]
        #print("For this task ratios:", task_ratios)

        self.average_task_ratios.append(sum(task_ratios) / len(task_ratios))
        self.worst_task_ratios.append(max(task_ratios))
        #print("Average ratio for each task:", average_task_ratio)
        #print("Worst ratio for each task:", worst_task_ratio)

        deletion_task_ratios = [del_cost / opt_cost for del_cost, opt_cost in zip(deletion_costs, optimal_costs)]
        #print("For this task deletion ratios:", deletion_task_ratios)

        self.average_deletion_ratios.append(sum(deletion_task_ratios) / len(deletion_task_ratios))
        self.worst_deletion_ratios.append(max(deletion_task_ratios))
        #print("Average ratio for each deletion task:", average_deletion_ratio)
        #print("Worst ratio for each deletion task:", worst_deletion_ratio)

        #self.average_task_ratios.extend(average_task_ratio)
        #self.worst_task_ratios.extend(worst_ratio_for_each_task)
        #self.average_deletion_ratios.extend(deletion_average_ratio_for_each_task)
        #self.worst_deletion_ratios.extend(deletion_worst_ratio_for_each_task)

    def plot_data(self, average_task_ratios, worst_task_ratios, average_deletion_ratios, worst_deletion_ratios,
                    task_numbers, save_path=None):
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        fig.tight_layout(pad=3.0)

        # Plot average task ratios
        axs[0, 0].plot(task_numbers, average_task_ratios, marker='o', linestyle='--')
        axs[0, 0].set_title('Average Task Ratios')
        axs[0, 0].set_xlabel('Task Numbers')
        axs[0, 0].set_ylabel('Ratio')
        axs[0, 0].set_xticks(task_numbers)
        axs[0, 0].set_xticklabels(task_numbers)

        # Plot worst task ratios
        axs[0, 1].plot(task_numbers, worst_task_ratios, marker='o', linestyle='--')
        axs[0, 1].set_title('Worst Task Ratios')
        axs[0, 1].set_xlabel('Task Numbers')
        axs[0, 1].set_ylabel('Ratio')
        axs[0, 1].set_xticks(task_numbers)
        axs[0, 1].set_xticklabels(task_numbers)

        # Plot average deletion ratios
        axs[1, 0].plot(task_numbers, average_deletion_ratios, marker='o', linestyle='--')
        axs[1, 0].set_title('Average Deletion Ratios')
        axs[1, 0].set_xlabel('Task Numbers')
        axs[1, 0].set_ylabel('Ratio')
        axs[1, 0].set_xticks(task_numbers)
        axs[1, 0].set_xticklabels(task_numbers)

        # Plot worst deletion ratios
        axs[1, 1].plot(task_numbers, worst_deletion_ratios, marker='o', linestyle='--')
        axs[1, 1].set_title('Worst Deletion Ratios')
        axs[1, 1].set_xlabel('Task Numbers')
        axs[1, 1].set_ylabel('Ratio')
        axs[1, 1].set_xticks(task_numbers)
        axs[1, 1].set_xticklabels(task_numbers)

        if save_path:
            plt.savefig(save_path, dpi=300)

        plt.show()


if __name__ == '__main__':
    results_folder = 'results'
    graph_plot = GraphPlot()

    task_numbers = []

    files_in_folder = [filename for filename in os.listdir(results_folder) if filename.endswith("_tasks.csv")]

    sorted_files = sorted(files_in_folder, key=lambda x: int(x.split('_')[2].split('_')[0]) if x.split('_')[2].
                          split('_')[0].isdigit() else 0)

    for filename in sorted_files:
        file_path = os.path.join(results_folder, filename)
        algorithm_costs, deletion_costs, optimal_costs = graph_plot.read_costs_from_csv(file_path)
        graph_plot.calculate_data(algorithm_costs, deletion_costs, optimal_costs)

        task_number = int(filename.split('_')[2].split('_')[0]) if filename.split('_')[2].split('_')[0].isdigit() else 0
        task_numbers.append(task_number)

    print("\n")
    print("Task Numbers:", task_numbers)
    print("Average Task Ratio:", graph_plot.average_task_ratios)
    print("Worst Task Ratio:", graph_plot.worst_task_ratios)
    print("Average Deletion Ratio:", graph_plot.average_deletion_ratios)
    print("Worst Deletion Ratio:", graph_plot.worst_deletion_ratios)

    graph_plot.plot_data(graph_plot.average_task_ratios, graph_plot.worst_task_ratios,
                         graph_plot.average_deletion_ratios, graph_plot.worst_deletion_ratios, task_numbers,
                         save_path='results/graphs.png')


