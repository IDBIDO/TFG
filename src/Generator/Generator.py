import json

import numpy as np

import item_prob_func

# function to generate the probability vector
print(item_prob_func.prob_method)


class Generator:
    def __init__(self):
        data = Generator.read_config()

        # general
        self._item_num = data.get("item_num")
        self._stream_size = self._item_num/data.get("item_proportion")

        # probability function var
        self._prob_func = Generator.get_prob_func(data.get("prob_func"))
        self._zipf_alpha = data.get("zipf_alpha")

        # probability vector
        self.prob_array = None

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

        # generate item distribution properties

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
        with open('../../config/generator_config.json', 'r') as json_file:
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