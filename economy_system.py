import json


def on_reg(user_id):
    data = json.load(open('balances.json'))
    if str(user_id) in data:
        return False
    else:
        with open('balances.json', 'w') as file:
            data[str(user_id)] = 10000
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True


def balance(user_id, transfer_mode=None):
    if str(user_id) not in json.load(open('balances.json')):
        return False
    else:
        if transfer_mode:
            return json.load(open('balances.json'))[str(user_id)]
        else:
            return '{:,}'.format(json.load(open('balances.json'))[str(user_id)]).replace(',', '.')


def add(user_id, amount):
    data = json.load(open('balances.json'))
    if str(user_id) not in data:
        with open('balances.json', 'w') as file:
            data[str(user_id)] = amount
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True
    else:
        with open('balances.json', 'w') as file:
            data[str(user_id)] = data[str(user_id)] + amount
            json.dump(data, file, indent=2, ensure_ascii=False)
        return True


def remove(user_id, amount):
    data = json.load(open('balances.json'))
    with open('balances.json', 'w') as file:
        data[str(user_id)] = data[str(user_id)] - amount
        json.dump(data, file, indent=2, ensure_ascii=False)
    return True
