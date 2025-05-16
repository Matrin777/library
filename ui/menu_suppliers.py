from models.author import get_all_authors, get_author_by_id
from models.author import Author

def menu_authors():
    while True:
        print("\n=== Авторы ===")
        print("1. Показать всех авторов")
        print("2. Добавить автора")
        print("3. Удалить автора")
        print("4. Изменить автора")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            authors = get_all_authors()
            print("\nСписок авторов:")
            for a in authors:
                print(f"{a.codeauthor} - {a.name} {a.surname}")
        elif choice == "2":
            name = input("Имя автора: ").strip()
            surname = input("Фамилия автора: ").strip()
            author = Author(name=name, surname=surname)
            author.save()
            print("Автор добавлен.")
        elif choice == "3":
            code = input("Введите ID автора для удаления: ").strip()
            author = get_author_by_id(int(code))
            if author:
                author.delete()
                print("Автор удален.")
            else:
                print("Автор не найден.")
        elif choice == "4":
            code = input("Введите ID автора для редактирования: ").strip()
            author = get_author_by_id(int(code))
            if author:
                new_name = input(f"Новое имя ({author.name}): ").strip()
                new_surname = input(f"Новая фамилия ({author.surname}): ").strip()
                if new_name:
                    author.name = new_name
                if new_surname:
                    author.surname = new_surname
                author.save()
                print("Автор обновлен.")
            else:
                print("Автор не найден.")
        elif choice == "0":
            break
        else:
            print("Неверный выбор.")