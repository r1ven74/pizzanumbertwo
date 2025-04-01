from model import *
from view import *

def run_main_loop():
    users = load_users()
    admin_password = "adminkapriydi"

    while True:
        show_main_menu()
        choice = input("Выберите действие: ")

        if choice == '1':
            name, password, birth_year = register_user_view()
            success, message = register_user(name, password, birth_year)
            display_message(message)
            if success:
                users[name] = {'password': password, 'birth_year': birth_year}

        elif choice == '2':
            name = input("Введите ваше имя для заказа: ")
            if name not in users:
                display_message("Сначала необходимо зарегистрироваться.")
                continue

            password = input("Введите пароль: ")
            if password != users[name]['password']:
                display_message("Неверный пароль. Попробуйте снова.")
                continue
            is_adult = is_user_adult(users[name]['birth_year'])
            menu = get_menu(is_adult)
            if is_adult:
                display_message("Выберите пиццу или напиток:")
            else:
                display_message("Выберите пиццу:")
            orders = pizza_selection_view(menu)

            if orders:
                receipt = generate_receipt(name, orders)
                print(receipt)
                break

        elif choice == '3':
            admin_input = input("Введите пароль админа: ")
            if admin_input == admin_password:
                run_admin_menu()
            else:
                print("Неверный пароль.")

        elif choice == '4':
            print("Выход из программы.")
            break

        else:
            display_message("Неверный выбор, попробуйте снова.")
