from models.order import Order, get_all_orders, get_order_by_id
from models.client import get_all_clients
from models.book import get_all_books, get_book_by_code
from models.order_item import OrderItem, get_items_by_order_id
from datetime import datetime

def manage_order_items(order_id):
    while True:
        print("\n=== Позиции заказа ===")
        items = get_items_by_order_id(order_id)
        if not items:
            print("Нет позиций.")
        else:
            for item in items:
                product = get_book_by_code(item.product_id)
                product_name = product.name if product else "N/A"
                print(f"{item.id}. {product_name} | Кол-во: {item.quantity} | Цена за единицу: {item.item_price} руб.")

        print("\nДоступные действия:")
        print("1. Добавить позицию")
        print("2. Удалить позицию")
        print("3. Изменить позицию")
        print("0. Назад к заказу")
        choice = input("Выберите действие: ")

        if choice == "1":
            books = get_all_books()
            if not books:
                print("Нет доступных книг для добавления.")
                continue
            print("\nДоступные книги:")
            for b in books:
                print(f"{b.codebook}. {b.name} - {b.price} руб.")
            try:
                product_id = int(input("Введите ID книги: "))
                product = get_book_by_code(product_id)
                if not product:
                    print("Книга с таким ID не найдена.")
                    continue
            except:
                print("Некорректный ввод ID.")
                continue
            try:
                quantity = int(input("Введите количество: "))
                if quantity <= 0:
                    print("Количество должно быть положительным числом.")
                    continue
            except:
                print("Некорректный ввод количества.")
                continue
            item_price = product.price
            new_item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
                item_price=item_price
            )
            new_item.save()
            print("✅ Позиция добавлена.")
        elif choice == "2":
            try:
                item_id = int(input("Введите ID позиции для удаления: "))
            except:
                print("Некорректный ввод ID.")
                continue
            item = next((i for i in get_items_by_order_id(order_id) if i.id == item_id), None)
            if item:
                item.delete()
                print("Позиция удалена.")
            else:
                print("❌ Позиция не найдена.")
        elif choice == "3":
            try:
                item_id = int(input("Введите ID позиции для редактирования: "))
            except:
                print("Некорректный ввод ID.")
                continue
            items = get_items_by_order_id(order_id)
            item = next((i for i in items if i.id == item_id), None)
            if not item:
                print("❌ Позиция не найдена.")
                continue
            try:
                new_quantity = int(input("Новое количество: "))
                if new_quantity <= 0:
                    print("Количество должно быть положительным числом.")
                    continue
            except:
                print("Некорректный ввод.")
                continue
            item.quantity = new_quantity
            item.save()
            print("Позиция обновлена.")
        elif choice == "0":
            break
        else:
            print("❌ Неверный ввод.")
def menu_orders():
    while True:
        print("\n=== Заказы ===")
        print("1. Показать все заказы")
        print("2. Добавить заказ")
        print("3. Удалить заказ")
        print("4. Управление позициями заказа")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ")

        if choice == "1":
            orders = get_all_orders()
            if not orders:
                print("\nНет заказов.")
            else:
                print("\nСписок заказов:")
                for o in orders:
                    print(f"{o.id}. Клиент ID: {o.client_id} | Дата: {o.order_date} | Сумма: {o.total_amount:.2f} руб.")
        elif choice == "2":
            clients = get_all_clients()
            if not clients:
                print("Нет доступных клиентов для создания заказа.")
                continue
            print("\nДоступные клиенты:")
            for c in clients:
                print(f"{c.codeclient}. {c.name} {c.surname}")
            try:
                client_id = int(input("Введите ID клиента: "))
                if not any(c.codeclient == client_id for c in clients):
                    print("Клиент с таким ID не найден.")
                    continue
            except:
                print("Некорректный ввод ID.")
                continue
            order_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order = Order(client_id=client_id, total_amount=0.0, order_date=order_date_str)
            order.save()
            manage_order_items(order.id)
            items = get_items_by_order_id(order.id)
            total_sum = sum(i.quantity * i.item_price for i in items)
            order.total_amount = total_sum
            order.save()
            print(f"Сумма заказа: {total_sum:.2f} руб.")
        elif choice == "3":
            try:
                order_id_del = int(input("Введите ID заказа для удаления: "))
            except:
                print("Некорректный ввод ID.")
                continue
            order_to_delete = get_order_by_id(order_id_del)
            if order_to_delete:
                order_to_delete.delete()
                print("Заказ удален.")
            else:
                print("❌ Заказ не найден.")
        elif choice == "4":
            try:
                order_id_manage = int(input("Введите ID заказа для управления позициями: "))
            except:
                print("Некорректный ввод.")
                continue
            existing_order = get_order_by_id(order_id_manage)
            if not existing_order:
                print("❌ Заказ не найден.")
                continue
            manage_order_items(order_id_manage)
        elif choice == "0":
            break
        else:
            print("❌ Неверный ввод.")