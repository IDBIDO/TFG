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

    def plot(self):
        """
        Plot the data in 2D using matplotlib.
        """
        x = self.getx()
        y = self.gety()
        labels = self.get_label()
        colors = ['red' if label == -1 else 'blue' for label in labels]
        plt.scatter(x, y, label='Data Points', color=colors, marker='.')
        # Set plot labels
        plt.xlabel('Attribute1 (x)')
        plt.ylabel('Attribute2 (y)')
        plt.title('Scatter Plot of Attribute1 vs. Attribute2')
        # Display the plot
        plt.legend()
        plt.grid(True)
        plt.show()




if __name__ == "__main__":
    root = get_project_root()
    print(root)
    st = str(root)
    print(st + "/data/float_data.csv")
    a = RawDataPlotter2D(st + "/data/float_data.csv")
    print(a.get_label())

    a.plot()
