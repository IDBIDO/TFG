import os

import pandas as pd


class DataManager:
    def __init__(self, file_name, option):

        self.path = '../../data/' + file_name
        self.header = ["id", "value", "anomaly"]
        # check if the file exists
        if not os.path.exists(self.path):
            if option == 'r':
                raise Exception("File does not exist")
            if option == 'w':
                # create csv file
                open(self.path, 'w+')

                self.write_line(self.header)
                print("File %s created successfully" % self.path)

        self.data = None
        if option == 'r':
            self.load_data()

    def load_data(self):
        self.data = pd.read_csv(self.path, dtype={"id": int, "value": float, "anomaly": int})

    def write_line(self, line):
        line_df = pd.DataFrame([line])
        line_df.to_csv(self.path, mode='a', header=False, index=False)

    def get_data(self):
        return self.data

    @staticmethod
    def list_data_files():
        return os.listdir('../../data')

    @staticmethod
    def delete_data_file(file_name):
        # mensage to user to confirm the deletion
        print("Are you sure you want to delete the file %s? (y/n)" % file_name)
        # get the user input
        user_input = input()
        # check if the user wants to delete the file
        if user_input == 'y':
            # delete the file
            os.remove('../../data/' + file_name)
            print("File %s deleted successfully" % file_name)


if __name__ == '__main__':
    a = DataManager('test.csv', 'w')
    a.write_line([1, 2, 3])
    b = DataManager('test.csv', 'r')
    print(b.get_data())
