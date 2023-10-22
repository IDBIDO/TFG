import json

import numpy as np
from matplotlib import pyplot as plt

import item_prob_func
from scipy import stats
# function to generate the probability vector
print(item_prob_func.prob_method)


class Generator:
    def __init__(self):
        data = Generator.read_config()

        # general
        self._item_num = data.get("item_num")
        self._stream_size = self._item_num / data.get("item_proportion")

        # probability function var
        self._prob_func = Generator.get_prob_func(data.get("prob_func"))
        self._zipf_alpha = data.get("zipf_alpha")

        # probability vector
        self.prob_array = None

        # item distribution
        self.distribution = data.get("distribution")
        self.normal_mean = data.get("normal_mean")
        self.normal_std = data.get("normal_std")
        self.outlier_threshold = data.get("outlier_threshold")

    def generate_prob_vector(self):
        print(self._prob_func.__name__)
        if 'zipf' in self._prob_func.__name__:
            self.prob_array = self._prob_func(self._item_num, self._zipf_alpha)
        else:
            self.prob_array = self._prob_func(self._item_num)

    def convert_prob_to_num(self):
        # convert probability to number of items(self._stream_size)
        scaled_values = np.array(self.prob_array) * self._stream_size
        self.prob_array = np.round(scaled_values).astype(int)

    def generate(self):
        # generate the probability vector
        self.generate_prob_vector()
        print(self.prob_array)

        # convert probability to number of items
        self.convert_prob_to_num()
        print(self.prob_array)
        print(np.sum(self.prob_array))
        # plot the distribution line chart
        plt.plot(self.prob_array)
        plt.show()



        # generate item distribution properties
        if 'normal' in self.distribution:
            # generate noraml distribution with self.prob_array[i] num and self.normal_mean and self.normal_std std

            data_value = np.empty(np.sum(self.prob_array), dtype=np.float64)
            data_anomaly = np.zeros(np.sum(self.prob_array), dtype=np.int8)
            for i in range(self._item_num):
                # mean is number random in interval [self.normal_mean[0], self.normal_std[1]]
                # std is number random in interval [self.normal_std[0], self.normal_std[1]]
                mean = np.random.uniform(self.normal_mean[0], self.normal_mean[1])
                std = np.random.uniform(self.normal_std[0], self.normal_std[1])

                # print("mean = %f, std = %f" % (mean, std))
                current_data = np.random.normal(mean, std, self.prob_array[i])
                print(current_data)
                z_scores = stats.zscore(current_data)
                outliers_index = np.where(np.abs(z_scores) > self.outlier_threshold)
                for index in outliers_index:
                    print(current_data[outliers_index], end=', ')
                print("\n")
                # print(r)
                # #plot the distribution r
                # count, bins, ignored = plt.hist(r, 30, density=True)
                # plt.plot(bins, 1 / (std * np.sqrt(2 * np.pi)) *
                #             np.exp(- (bins - mean) ** 2 / (2 * std ** 2)),
                #             linewidth=2, color='r')
                # plt.show()

    def test(self):
        print(self._prob_func)

    @staticmethod
    def get_prob_func(function_name):
        for func in item_prob_func.prob_method:
            if function_name in func.__name__:
                return func
        return None

    @staticmethod
    def read_config():
        # Open the JSON file in read mode
        with open('../../config/generator_config_old.json', 'r') as json_file:
            # Read JSON data from the file
            data = json.load(json_file)

        # Now, 'data' contains the parsed JSON content as a Python data structure
        # You can work with 'data' as a dictionary or a list depending on the JSON structure
        # print(data)
        # print(data.get("zipf_alpha"))
        return data


a = Generator()
a.test()

a.generate()
