import pandas as pd
import os


def maketotal():
    root_path = 'c101010100-p100101'
    for path in os.listdir(root_path):
        file = pd.read_csv(os.path.join(root_path, path))
        file.to_csv("{}/total.csv".format(root_path), mode='a')

def anaylise():
    data: pd.DataFrame = pd.read_csv('c101010100-p100101/total.csv')
    data.fillna("??")
    print(data.describe())




anaylise()
        

