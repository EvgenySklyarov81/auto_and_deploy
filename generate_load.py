import numpy as np
import pandas as pd
import random
import string
import psycopg2
import glob
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
FILES_PATH = config['Files']['FILES_PATH']
DB_CREDS = config['DataBase']

# создание папки для файлов
try:
    os.mkdir(FILES_PATH)
except FileExistsError:
    pass

# имена файлов, товары, категории, возможные размеры скидок
files = [f'{i}_{j}' for i in range(1, 4) for j in range(1, 3)]

products = {
    'Food': ['Bread', 'Meat', 'Milk', 'Beer', 'Candy', 'Fish', 'Cheese'],
    'Toys': ['Ball', 'Lego', 'Spinner', 'Doll', 'Chess', 'Toy car', 'Kite'],
    'Misc': ['Shovel', 'Gloves', 'Light bulb', 'Wig', 'Bucket', 'Lighter', 'Oil']
}

discounts = np.arange(0, 0.51, 0.1)

def generate_id():
    """ Генерирует 6-ти символьный идентификатор """
    letters = random.choices(string.ascii_lowercase, k=3)
    digits = random.choices(string.digits, k=3)
    symbols = letters + digits
    random.shuffle(symbols)
    return ''.join(symbols)

def generate_data(files):
    """ Построчно генерирует данные для каждого файла """
    for file in files:
        rows = random.randint(5, 20)
        ids = [generate_id() for _ in range(rows // 2)]
        index = range(rows)
        columns = ["doc_id", "item", "category", "amount", "price", "discount"]
        df = pd.DataFrame(index=index, columns=columns)
        
        for i in range(rows):
            doc_id  = random.choice(ids)
            category = random.choice([*products])
            item = random.choice(products[category])
            amount = random.randrange(1, 11)
            price = random.randrange(1, 101)
            discount = price * round(np.random.choice(discounts), 1)

            df.iloc[i] = doc_id, item, category, amount, price, discount
        df.to_csv(f'{FILES_PATH}/{file}.csv', index=False, header=False)

# генерация файлов с данными
generate_data(files)

# запись данных из файлов в БД
conn = psycopg2.connect(host=DB_CREDS['HOST'], dbname=DB_CREDS['DATABASE'],  user=DB_CREDS['USER'], password=DB_CREDS['PASSWORD'])
cur = conn.cursor()

insert_query = """
               insert into sales values(%s, %s, %s, %s, %s, %s);
               """
data_sets = glob.glob(f'{FILES_PATH}/*.csv')

for data_set in data_sets:
    with open(data_set) as f:
        for line in f:
            values = line.strip().split(',')
            cur.execute(insert_query, values)

conn.commit()
cur.close()
conn.close()