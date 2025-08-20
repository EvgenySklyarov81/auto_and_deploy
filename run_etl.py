import os
import glob
import configparser
import numpy as np
from generate_data import generate_data
from load_data import load_data

# имена файлов
files = [f'{i}_{j}' for i in range(1, 4) for j in range(1, 3)]

# товары, категории
products = {
    'Food': ['Bread', 'Meat', 'Milk', 'Beer', 'Candy', 'Fish', 'Cheese'],
    'Toys': ['Ball', 'Lego', 'Spinner', 'Doll', 'Chess', 'Toy car', 'Kite'],
    'Misc': ['Shovel', 'Gloves', 'Light bulb', 'Wig', 'Bucket', 'Lighter', 'Oil']
}

# возможные размеры скидок
discounts = np.arange(0, 0.51, 0.1)

dirname = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))


# создание папки для файлов
try:
    os.mkdir('data')
except FileExistsError:
    pass

generate_data(files, products, discounts)

db_connect = config['DATABASE']
data_sets = glob.glob(f'data/*.csv')

load_data(db_connect, data_sets)