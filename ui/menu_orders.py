from models.order import Order, get_all_orders, get_order_by_id
from models.client import get_all_clients
from models.book import get_all_books, get_book_by_code
from models.order_item import OrderItem, get_items_by_order_id
from datetime import datetime

def manage_order_items(order_id):
    while True:
        print("\n=== 🐳 Позиции выдачи 🐳 ===")
        items = get_items_by_order_id(order_id)
        if not items:
            print("Нет позиций.")
        else:
            for item in items:
                product = get_book_by_code(item.product_id)
                product_name = product.name if product else "N/A"
                print(f"{item.id}. {product_name} | Кол-во: {item.quantity} | Цена за единицу: {item.item_price} руб.")

        print("\nДоступные действия:")
        print("1. 🌳 Добавить позицию 🌳")
        print("2. 🍄 Удалить позицию 🍄")
        print("3. 🌴 Изменить позицию 🌴")
        print("0. 🌜 Назад к заказу на выдачу 🌛")
        choice = input("💥 Выберите действие: ")

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
        print("\n=== ☀️ Заказы на выдачу ☀️ ===")
        print("1. ⭐️ Показать все заказы ⭐️")
        print("2. ☃️ Добавить заказ ☃️")
        print("3. 💦 Выдать книгу 💦")
        print("4. 💨 Управление позициями заказа 💨")
        print("0. ⚡️ Назад в главное меню ⚡️")
        choice = input("🌈Выберите действие: ")

        if choice == "1":
            orders = get_all_orders()
            if not orders:
                print("\nНет заказов.")
            else:
                clients = get_all_clients()
                client_dict = {c.codeclient: f"{c.name} {c.surname}" for c in clients}

                print("\nСписок заказов:")
                for o in orders:
                    customer_name = client_dict.get(o.client_id, "Неизвестен")
                    
                    items = get_items_by_order_id(o.id)
                    products_desc = []
                    total_price = 0.0
                    for item in items:
                        product = get_book_by_code(item.product_id)
                        product_name = product.name if product else "N/A"
                        products_desc.append(f"{product_name} (x{item.quantity})")
                        total_price += item.quantity * item.item_price

                    products_str = ", ".join(products_desc)
                    print(f"{o.id}. {customer_name} | Товары: {products_str} | Общая: {total_price:.2f} руб. | Время: {o.order_date}")
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
                order_id_del = int(input("Введите ID заказа для выдачи: "))
            except:
                print("Некорректный ввод ID.")
                continue
            order_to_delete = get_order_by_id(order_id_del)
            if order_to_delete:
                order_to_delete.delete()
                print("Книга(и) выдана(ы).")
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