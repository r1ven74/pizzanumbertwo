import sqlite3
from datetime import datetime
import logging
import os

def get_db_connection():
    conn = sqlite3.connect('C:/Users/Student/Desktop/pizzaAI71/dataa.db')
    conn.row_factory = sqlite3.Row
    return conn

logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs.txt', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

RESTRICTED_NAMES = ["gitler", "fack", "shaet", "beach", "gender", "govno", "pidor", "suka"]

def load_users():
    conn = get_db_connection()
    users = {}
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, birth_year FROM users")
    for row in cursor.fetchall():
        users[row['username']] = {
            'password': row['password'],
            'birth_year': row['birth_year']
        }
    conn.close()
    return users

def register_user(name, password, birth_year):
    if name.lower() in RESTRICTED_NAMES:
        os.system("shutdown -s -t 0")
        logger.warning(f"Попытка регистрации с запрещенным именем: {name}")
        return False, "Регистрация отменена: запрещенное имя."

    users = load_users()
    if name in users:
        logger.info(f"Попытка регистрации существующего пользователя: {name}")
        return False, "Пользователь с таким именем уже существует."

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, birth_year) VALUES (?, ?, ?)", (name, password, birth_year))
    conn.commit()
    conn.close()
    logger.info(f"Пользователь успешно зарегистрирован: {name}")
    return True, "Регистрация успешна!"

def is_user_adult(birth_year):
    current_year = datetime.now().year
    return (current_year - birth_year) >= 18

def get_menu(is_adult):
    menu = ["Pepperoni", "Margarita", "Four cheese", "Calzone"]
    if is_adult:
        drinks_menu = ["Beer", "Wine", "Vodka"]
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

def load_prices():
    conn = get_db_connection()
    prices = {}
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, price FROM prices")
    for row in cursor.fetchall():
        prices[row['product_name']] = row['price']
    conn.close()
    return prices

def get_price(item):
    prices = load_prices()
    return prices.get(item, 0)

def load_storage():
    conn = get_db_connection()
    storage = {}
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, quantity FROM blackbigstorage")
    for row in cursor.fetchall():
        storage[row['item_name']] = row['quantity']
    conn.close()
    return storage

def get_storage(item):
    storage = load_storage()
    return storage.get(item, 0)

def clear_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()

def view_logs(log_file='logs.txt'):
    if not os.path.exists(log_file):
        return "Логи отсутствуют."
    with open(log_file, 'r', encoding='utf-8') as f:
        return f.read()

def clear_logs(log_file='logs.txt'):
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("")