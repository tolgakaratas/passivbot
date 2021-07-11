import datetime
import json

import hjson


def sort_dict_keys(d):
    if type(d) == list:
        return [sort_dict_keys(e) for e in d]
    if type(d) != dict:
        return d
    return {key: sort_dict_keys(d[key]) for key in sorted(d)}


def ts_to_date(timestamp: float) -> str:
    return str(datetime.datetime.fromtimestamp(timestamp)).replace(' ', 'T')


def print_(args, r=False, n=False):
    line = str(datetime.datetime.now()) + '  '
    str_args = '{} ' * len(args)
    line += str_args.format(*args)
    if n:
        print('\n' + line, end=' ')
    elif r:
        print('\r' + line, end=' ')
    else:
        print(line)
    return line


def load_key_secret(exchange: str, user: str) -> (str, str):
    try:
        keyfile = json.load(open('api-keys.json'))
        # Checks that the user exists, and it is for the correct exchange
        if user in keyfile and keyfile[user]["exchange"] == exchange:
            keyList = [str(keyfile[user]["key"]), str(keyfile[user]["secret"])]
            return keyList
        elif user not in keyfile or keyfile[user]["exchange"] != exchange:
            print_(["Looks like the keys aren't configured yet, or you entered the wrong username!"], n=True)
        raise Exception('API KeyFile Missing!')
    except FileNotFoundError:
        print_(["File not found!"], n=True)
        raise Exception('API KeyFile Missing!')


def load_base_config(path: str) -> dict:
    try:
        config = hjson.load(open(path))
        return config
    except Exception as e:
        print_(["Could not read config", e], n=True)
        return {}


def add_or_append(dict, key, value):
    if key in dict:
        dict[key].append(value)
    else:
        dict[key] = [value]
    return dict


def print_order(order):
    print('Symbol', order.symbol)
    print('Order_id', order.order_id)
    print('Price', order.price)
    print('Qty', order.qty)
    print('Type', order.type)
    print('Side', order.side)
    print('Timestamp', order.timestamp)
    print('Action', order.action)
    print('Position_side', order.position_side)


def print_position(position):
    print('Symbol', position.symbol)
    print('Size', position.size)
    print('Price', position.price)
    print('Liquidation_price', position.liquidation_price)
    print('Upnl', position.upnl)
    print('Leverage', position.leverage)
    print('Position_side', position.position_side)


def print_order_list(order_list):
    print('Long:')
    for order in order_list.long:
        print_order(order)
    print('Short:')
    for order in order_list.short:
        print_order(order)


def print_position_list(position_list):
    print('Long:')
    print_position(position_list.long)
    print('Short:')
    print_position(position_list.short)
