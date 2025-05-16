from models.client import get_all_clients, get_client_by_id
from models.client import Client

def menu_clients():
    while True:
        print("\n=== Клиенты ===")
        print("1. Показать всех клиентов")
        print("2. Добавить клиента")
        print("3. Удалить клиента")
        print("4. Изменить клиента")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            clients = get_all_clients()
            print("\nСписок клиентов:")
            for c in clients:
                print(f"{c.codeclient} - {c.name} {c.surname}")
        elif choice == "2":
            name = input("Имя: ").strip()
            surname = input("Фамилия: ").strip()
            telephone = input("Телефон: ").strip()
            client = Client(name=name, surname=surname, telephone=telephone)
            client.save()
            print("Клиент добавлен.")
        elif choice == "3":
            code = input("Введите ID клиента для удаления: ").strip()
            client = get_client_by_id(int(code))
            if client:
                client.delete()
                print("Клиент удален.")
            else:
                print("Клиент не найден.")
        elif choice == "4":
            code = input("Введите ID клиента для редактирования: ").strip()
            client = get_client_by_id(int(code))
            if client:
                new_name = input(f"Новое имя ({client.name}): ").strip()
                new_surname = input(f"Новая фамилия ({client.surname}): ").strip()
                new_tel = input(f"Новый телефон ({client.telephone}): ").strip()
                if new_name:
                    client.name = new_name
                if new_surname:
                    client.surname = new_surname
                if new_tel:
                    client.telephone = new_tel
                client.save()
                print("Клиент обновлен.")
            else:
                print("Клиент не найден.")
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")