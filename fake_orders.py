import json
import numpy as np
import os
import pandas as pd

from faker import Faker
from pprint import pprint


fake = Faker()

DELETE_ATTR = ('order_date', 'priority', 'quantity')
# PRIORITY = ('L', 'M', 'H')
PRIORITY = ('LOW', 'HIGH')
PRODUCTS = ('Laptop', 'GPU', 'Plant', 'Floppy', 'Chair')


# order structure:
# 'order_id': {
#     'order_date': 'date str ISO8601',  <- REMOVED
#     'priority': 'str',
#     'quantity': 'int'
# }

def generate_fake_orders(limit, not_tidy = True):
    err_0, err_1, err_2 = 0, 0, 0
    orders = {}

    high_priority = 0

    Faker.seed(42)
    for i in range(limit):
        # order_id = fake.ean(length = 8, prefixes = ('000', ))
        order_id = i + 1
        # order_date = fake.date_between(start_date = '-10d').isoformat()
        # order_priority = PRIORITY[np.random.randint(0, len(PRIORITY))]
        order_priority = 'LOW'
        product = PRODUCTS[np.random.randint(0, len(PRODUCTS))]
        quantity = np.random.randint(1, 90)

        if fake.boolean(chance_of_getting_true = 25) and high_priority <= 25:
            high_priority += 1
            order_priority = 'HIGH'

        # orders[order_id] = {'order_date': order_date, 'priority': order_priority, 'product': product, 'quantity': quantity}
        orders[order_id] = {'priority': order_priority, 'product': product, 'quantity': quantity}


        # mess up the data - 10% chance
        if not_tidy and fake.boolean(chance_of_getting_true = 10):
            rand_val = np.random.randint(0, 3)

            if rand_val == 0:  # remove a random attribute from the order
                orders[order_id].pop(DELETE_ATTR[np.random.randint(0, 3)])
                err_0 += 1

            elif rand_val == 1:  # change priority
                orders[order_id]['priority'] = 'Y'
                err_1 += 1

            else:  # replace date with only a year
                orders[order_id]['order_date'] = '2021'
                err_2 += 1

    # print(err_0, err_1, err_2)
    print(high_priority)

    with open(os.getcwd() + '/order_data_NEW_2.json', 'w') as f_out:
        json.dump(orders, f_out, indent = 4)

def count(f_name):
    data = {}

    with open(f_name, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(data).T

    pprint(df['product'].value_counts())
    pprint(df['priority'].value_counts())


# generate_fake_orders(100)
# generate_fake_orders(100, False)

count(os.getcwd() + '/order_data_2.json')