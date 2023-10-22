import json


class GenConfig:

    def __init__(self):
        self.data = GenConfig.read_config()


    def print(self):
        print()

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

