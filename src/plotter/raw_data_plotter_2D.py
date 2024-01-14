import math

from src import mdcgenpy as mdc
import matplotlib.pyplot as plt
from src.utils import get_project_root


class RawDataPlotter2D:
    def __init__(self, path):
        self._path = path
        self._data, self._y = mdc.mdcgenutils.read_data_and_label(path)


    def getx(self):
        return self._data[:, 0]

    def gety(self):
        return self._data[:, 1]

    def get_label(self):
        return self._y


    # ...

    def plot(self):
        """
        Plot the data in 2D using matplotlib with unique colors for each label.
        """
        x = self.getx()
        y = self.gety()
        labels = self.get_label()

        unique_labels = set(labels)
        num_labels = len(unique_labels)
        color_map = plt.get_cmap('tab10', num_labels)  # You can use other colormaps

        plt.figure(figsize=(8, 6))  # Adjust the figure size as needed

        for i, label in enumerate(unique_labels):
            label_indices = (labels == label)
            plt.scatter(x[label_indices], y[label_indices], label=f'Label {label}', color=color_map(i), marker='.')

        # Set plot labels
        plt.xlabel('Attribute1 (x)')
        plt.ylabel('Attribute2 (y)')
        plt.title('Scatter Plot of Attribute1 vs. Attribute2')

        # Display the plot
        #plt.legend()
        plt.grid(True)
        plt.show()

    def generate_periodic_plots(self, n):
        """
        Generate periodic plots by grouping every n instances.

        Args:
            n (int): Number of instances to group.
        """
        total_instances = len(self._data)
        num_plots = math.ceil(total_instances/n)
        num_rows = math.ceil(num_plots / 3)  # Assuming 3 columns in the matrix

        fig, axes = plt.subplots(num_rows, 3, figsize=(15, 5 * num_rows), sharex=True, sharey=True)
        fig.suptitle(f"Special Plots (Grouped by {n} Instances)", fontsize=16)

        for i in range(num_plots):
            current_x = self.getx()[i*n:i*n+n]
            print(i*n)
            current_y = self.gety()[i*n:i*n+n]
            axes[i // 3, i % 3].scatter(current_x, current_y, marker='.')
            axes[i // 3, i % 3].set_title(f'Period {i}')
            print(f'Period {i}: {current_x}, {current_y}')
        plt.show()

    def generate_special_plots(self, n, save_path="special_plots.png"):
        """
        Generate special plots by grouping every n instances.

        Args:
            n (int): Number of instances to group.
            save_path (str): Path to save the generated image.
        """
        total_instances = len(self._data)
        num_plots = math.ceil(total_instances/2000)
        num_rows = math.ceil(total_instances/2000 / 3)  # Assuming 3 columns in the matrix

        fig, axes = plt.subplots(num_rows, 3, figsize=(15, 5 * num_rows))
        fig.suptitle(f"Special Plots (Grouped by {n} Instances)", fontsize=16)

        for i in range(num_plots):
            ax = axes[i // 3, i % 3]
            x_subset = self.getx()[i:i+n]
            y_subset = self.gety()[i:i+n]
            labels_subset = self.get_label()[i:i+n]
            colors = ['red' if label == -1 else 'blue' for label in labels_subset]
            ax.scatter(x_subset, y_subset, label=f'Period {i // n}', color=colors, marker='.')
            ax.set_title(f'Group {i // n}')

        # Hide empty subplots
        for i in range(total_instances, num_rows * 3):
            fig.delaxes(axes.flatten()[i])

        # Set plot labels
        fig.text(0.5, 0.04, 'Attribute1 (x)', ha='center', va='center')
        fig.text(0.06, 0.5, 'Attribute2 (y)', ha='center', va='center', rotation='vertical')

        # Adjust layout
        fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])

        # Display the plot
        plt.show()

        # Save the figure
        fig.savefig(save_path)




if __name__ == "__main__":
    root = get_project_root()
    print(root)
    st = str(root)
    print(st + "/data/float_data.csv")
    a = RawDataPlotter2D("float_data.csv")
    print(a.get_label())

    #a.plot()

    #a.generate_special_plots(2000)
    a.generate_periodic_plots(2000)