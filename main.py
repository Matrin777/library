from database.db_manager import initialize_db
from models.ganre import initialize_genres
from ui.menu import show_main_menu
from ui.menu_books import menu_books
from ui.menu_suppliers import menu_authors
from ui.menu_clients import menu_clients
from ui.menu_orders import menu_orders

def main():
    initialize_db()
    initialize_genres() 
    while True:
        choice = show_main_menu()
        if choice == "1":
            menu_books()
        elif choice == "2":
            menu_authors()
        elif choice == "3":
            menu_clients()
        elif choice == "4":
            menu_orders()
        elif choice == "0":
            print("Выход из программы. Бай Бай, Пупс😄!")
            break
        else:
            print("❌ Неверный ввод ❌")

if __name__ == "__main__":
    main()