import random
import csv


banks = ['Banco do Brasil', 'Banco Bradesco', 'Banco Itaú', 'Banco NuBank', 'Banco Santander']


def save_to_file():
    nome = f'./data/temp/teste_{random.randint(1, 999)}.csv'
    list_of_tr = generate_list()
    print(nome)
    with open(nome, 'w') as file:
        new_file = csv.writer(file, delimiter=',')
        for tr in list_of_tr:
            new_file.writerow(tr)


def generate_list():
    new_list = list()
    for transaction in range(random.randint(1, 200)):
        if len(new_list) == 0:
            transaction = generate_transaction()
        else:
            transaction = generate_transaction(new_list[0])
        new_list.append(transaction)
    return new_list


def generate_transaction(transaction=None):
    new_transaction = list()
    chance = random.randint(1, 100)
    # 01
    if transaction is None or chance > 80:
        origin_bank = banks[random.randint(0, len(banks)-1)]
    else:
        origin_bank = transaction[0]
    new_transaction.append(origin_bank)
    # 02
    if transaction is None or chance > 60:
        origin_agency = str(random.randint(1, 9999))
    else:
        origin_agency = transaction[1]
    oagclen = 4 - len(origin_agency)
    for char in range(oagclen):
        origin_agency = '0' + origin_agency
    new_transaction.append(origin_agency)
    # 03
    if transaction is None or chance > 60:
        origin_account = str(random.randint(1, 99999))
        oacclen = 5 - len(origin_account)
        for char in range(oacclen):
            origin_account = '0' + origin_account
        origin_account = origin_account + '-1'
    else:
        origin_account = transaction[2]
    new_transaction.append(origin_account)
    # 04
    if transaction is None or chance > 80:
        destination_bank = banks[random.randint(1, len(banks)-1)]
    else:
        destination_bank = transaction[3]
    new_transaction.append(destination_bank)
    # 05
    if transaction is None or chance > 60:
        destination_agency = str(random.randint(1, 9999))
    else:
        destination_agency = transaction[4]
    daglen = 4 - len(destination_agency)
    for char in range(daglen):
        destination_agency = '0' + destination_agency
    new_transaction.append(destination_agency)
    # 06
    if transaction is None or chance > 60:
        destination_account = str(random.randint(1, 99999))
        dacclen = 5 - len(destination_account)
        for char in range(dacclen):
            destination_account = '0' + destination_account
            destination_account = destination_account + '-1'
    else:
        destination_account = transaction[5]
    new_transaction.append(destination_account)
    # 07
    tr_pt_1_1 = random.randint(1, 99999)
    tr_pt_1_2 = random.randint(1, 999999)
    tr_pt_2 = random.randint(0, 99)
    if chance > 25:
        transaction_value = tr_pt_1_1 + (tr_pt_2 / 100)
    else:
        transaction_value = tr_pt_1_2 + (tr_pt_2 / 100)
    new_transaction.append(transaction_value)
    # 08
    month = str(random.randint(1, 12))
    mthlen = 2 - len(month)
    for char in range(mthlen):
        month = '0' + month
    day = str(random.randint(1, 28))
    daylen = 2 - len(day)
    for char in range(daylen):
        day = '0' + day
    chance = random.randint(1, 100)
    if transaction is None or chance > 75:
        transaction_date = f'2020-{month}-{day}T01:01:01'
    else:
        transaction_date = transaction[7]
    new_transaction.append(transaction_date)
    return new_transaction