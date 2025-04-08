from model import *
import logging


def display_message(message):
    print(message)

def show_main_menu():
    print("Главное меню:")
    print("1. Регистрация")
    print("2. Заказать пиццу")
    print("3. Админка")
    print("4. Выход")

def register_user_view():
    name = input("Введите ваше имя: ")
    password = input("Введите пароль: ")
    birth_year = int(input("Введите год рождения: "))
    logging.info(f"Пользователь указал данные для регистрации: {name}, {birth_year}")
    return name, password, birth_year

def pizza_selection_view(menu):
    conn = get_db_connection()
    cursor = conn.cursor()
    orders = {}
    while True:
        for index, item in enumerate(menu, start=1):
            print(f"{index}. {item}")

        choice = input("Выберите пункт (или введите 'готово' для завершения заказа): ")
        if choice.lower() == 'готово':
            break


        if choice.isdigit() and 1 <= int(choice) <= len(menu):
            item = menu[int(choice) - 1]
            quantity = int(input(f"Сколько {item} вы хотите заказать? "))
            price = get_price(item)
            if price > 0:
                orders[item] = (quantity, price)
                logging.info(f"Пользователь добавил в заказ: {item} (кол-во: {quantity})")
            else:
                print(f"Цена для {item} не найдена.")
        else:
            print("Неверный выбор, попробуйте еще раз.")
            logging.warning(f"Пользователь ввел неверный выбор: {choice}")
        if item == "Pepperoni":
            for i in range(1, 5):
                cursor.execute('UPDATE blackbigstorage SET quantity= quantity - ? WHERE id=?', (1 * quantity, i))
        elif item == "Margarita":
            for i in range(3, 8):
                cursor.execute('UPDATE blackbigstorage SET quantity= quantity - ? WHERE id=?', (1 * quantity, i))
            cursor.execute('UPDATE blackbigstorage SET quantity= quantity - ? WHERE id=?', (1 * quantity, 1))
        elif item == "Four cheese":
            for i in range(4):
                cursor.execute('UPDATE blackbigstorage SET quantity= quantity - ? WHERE id=?', (1 * quantity, 4))
            cursor.execute('UPDATE blackbigstorage SET quantity= quantity - ? WHERE id=?', (1 * quantity, 1))
        elif item == "Calzone":
            cursor.execute('UPDATE blackbigstorage SET quantity= quantity - ? WHERE id=?', (1 * quantity, 6))
            cursor.execute('UPDATE blackbigstorage SET quantity= quantity - ? WHERE id=?', (1 * quantity, 2))
            cursor.execute('UPDATE blackbigstorage SET quantity= quantity - ? WHERE id=?', (1 * quantity, 1))
        conn.commit()
        cursor.close()

    return orders

def run_admin_menu():
    while True:
        print("Настройки администрирования:")
        print("1. Просмотреть логи")
        print("2. Просмотреть пользователей")
        print("3. Очистить логи")
        print("4. Очистить пользователей")
        print("5. Назад в главное меню")

        admin_choice = input("Выберите действие: ")

        if admin_choice == '1':
            logs = view_logs()
            print("\n--- Логи ---")
            print(logs, "\n")
        elif admin_choice == '2':
            users = load_users()
            print("\n--- Пользователи ---")
            for name, details in users.items():
                print(f"Имя: {name}, Дата рождения: {details['birth_year']} \n")
        elif admin_choice == '3':
            clear_logs()
            print("Логи очищены.")
        elif admin_choice == '4':
            clear_users()
            print("Пользователи очищены.")
        elif admin_choice == '5':
            break
        else:
            print("Неверный выбор, попробуйте снова.")