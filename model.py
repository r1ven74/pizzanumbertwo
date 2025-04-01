import os
import json
from datetime import datetime
import logging
import sys
import io


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs.txt', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

STORAGE_FILE = "blackbigstorage.json"
USER_DATA_FILE = 'users.json'
PRICES_FILE = 'prices.json'
ADD_FILE = "blackbigadd.json"
RESTRICTED_NAMES = ["gitler", "fack", "shaet", "beach", "gender", "govno", "pidor", "suka"]

def load_users():
    if os.path.exists(USER_DATA_FILE) and os.path.getsize(USER_DATA_FILE) > 0:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

def load_prices():
    if os.path.exists(PRICES_FILE):
        with open(PRICES_FILE, 'r') as file:
            return json.load(file)
    return {"Pizza": {}, "Drinks": {}}

def add_storage():
    if os.path.exists(ADD_FILE):
        with open(ADD_FILE, 'r') as file:
            return json.load(file)
    return {"adatavion": {}}

def load_storage():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as file:
            return json.load(file)
    return {"store": {}}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)

def register_user(name, password, birth_year):
    if name.lower() in RESTRICTED_NAMES:
        os.system("shutdown -s -t 0")
        logger.warning(f"Попытка регистрации с запрещенным именем: {name}")
        return False, "Регистрация отменена: запрещенное имя."

    users = load_users()
    if name in users:
        logger.info(f"Попытка регистрации существующего пользователя: {name}")
        return False, "Пользователь с таким именем уже существует."

    users[name] = {'password': password, 'birth_year': birth_year}
    save_users(users)
    logger.info(f"Пользователь успешно зарегистрирован: {name}")
    return True, "Регистрация успешна!"

def is_user_adult(birth_year):
    current_year = datetime.now().year
    return (current_year - birth_year) >= 18

def get_menu(is_adult):
    menu = ["Pepperoni", "Margarita", "Four chesee", "Calcone"]
    if is_adult:
        drinks_menu = ["Pivo", "Vino", "Vodka"]
        menu.extend(drinks_menu)
    return menu

def generate_receipt(name, orders):
    total_price = 0
    receipt = (f"\nЧек для {name}:\n"
               f"\n====================================\n")
    for item, (quantity, price) in orders.items():
        item_total = quantity * price
        total_price += item_total
        receipt += f"- {item} (x{quantity}) по {price} руб. = {item_total} руб.\n"

    receipt += (f"Итоговая сумма: {total_price} руб.\nСпасибо за ваш заказ!"
                f"\n====================================")
    logger.info(f"Чек сгенерирован для {name}: {orders}")
    return receipt

def get_price(item):
    prices = load_prices()
    price = 0
    if item in prices['Pizza']:
        price = prices['Pizza'][item]
    elif item in prices['Drinks']:
        price = prices['Drinks'][item]
    return price

def get_add(item):
    adds = add_storage()
    add = 0
    if item in adds['adatavion']:
        add = adds['adatavion'][item]
    return add

def get_storage(item):
    storages = load_storage()
    storage = 0
    if item in storages['store']:
        storage = storages['store'][item]
    return storage

def load_users(file_path='users.json'):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users, file_path='users.json'):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(users, f)

def clear_users(file_path='users.json'):
    save_users({})

def view_logs(log_file='logs.txt'):
    if not os.path.exists(log_file):
        return "Логи отсутствуют."
    with open(log_file, 'r', encoding='utf-8') as f:
        return f.read()

def clear_logs(log_file='logs.txt'):
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("")
