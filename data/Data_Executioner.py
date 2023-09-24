import json
from itertools import zip_longest
from Data_Generator import DataGenerator
import csv
import io
import sys


def save_data_to_csv(num_tasks, instance_number):
    data_generator = DataGenerator(num_tasks, 40 + instance_number)  # seed
    intervals, demands, contributions, costs = data_generator.run()

    data_rows = []

    for interval, demand, contribution, cost in zip_longest(intervals, demands, contributions, costs, fillvalue=None):
        combined_value = f"{cost}, {json.dumps(interval)}"
        data_row = [combined_value, float(contribution) if contribution is not None else None,
                    int(demand) if demand is not None else None]
        data_rows.append(data_row)

    file_name = f"data/{num_tasks} tasks/instance{instance_number:02d}.csv"
    with io.open(file_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['bidding_profile', 'contribution', 'demand'])
        writer.writerows(data_rows)


if __name__ == "__main__":
    tasks_number = int(sys.argv[1])
    num_instances = int(sys.argv[2])

    for instance_number in range(1, num_instances + 1):
        save_data_to_csv(tasks_number, instance_number)
