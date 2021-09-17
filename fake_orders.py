import json
import numpy as np
import os

from faker import Faker


fake = Faker()

DELETE_ATTR = ('order_date', 'priority', 'quantity')
PRIORITY = ('L', 'M', 'H')

# order structure:
# 'order_id': {
#     'order_date': 'date str ISO8601',
#     'priority': 'str',
#     'quantity': 'int'
# }

def generate_fake_orders(limit, not_tidy = True):
    err_0, err_1, err_2 = 0, 0, 0
    orders = {}

    Faker.seed(42)
    for _ in range(limit):
        order_id = fake.ean(length = 8, prefixes = ('000', ))
        order_date = fake.date_between(start_date = '-10d').isoformat()
        order_priority = PRIORITY[np.random.randint(0, 3)]
        quantity = np.random.randint(1, 90)

        orders[order_id] = {'order_date': order_date, 'priority': order_priority, 'quantity': quantity}

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

    print(err_0, err_1, err_2)

    with open(os.getcwd() + '/order_data.json', 'w') as f_out:
        json.dump(orders, f_out, indent = 4)

generate_fake_orders(100)