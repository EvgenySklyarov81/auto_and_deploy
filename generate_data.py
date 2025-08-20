import numpy as np
import pandas as pd
import string
import random

def generate_id():
    """ Генерирует 6-ти символьный идентификатор """
    letters = random.choices(string.ascii_lowercase, k=3)
    digits = random.choices(string.digits, k=3)
    symbols = letters + digits
    random.shuffle(symbols)
    return ''.join(symbols)

def generate_data(files, products, discounts):
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
        
        df.to_csv(f'data/{file}.csv', index=False, header=False)