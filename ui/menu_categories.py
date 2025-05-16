from models.ganre import Ganre
from database.db_manager import get_connection

def menu_ganre():
    while True:
        print("\nМеню Жанров")
        print("1. Показать все жанры")
        print("2. Добавить жанр")
        print("3. Редактировать жанр")
        print("4. Удалить жанр")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ")

        if choice == '1':
            show_all_genres()
        elif choice == '2':
            add_genre()
        elif choice == '3':
            edit_genre()
        elif choice == '4':
            delete_genre()
        elif choice == '0':
            break
        else:
            print("Некорректный выбор, попробуйте снова.")

def show_all_genres():
    genres = Ganre.get_all_genres()
    if not genres:
        print("Жанры не найдены.")
        return
    print("\nСписок жанров:")
    for genre in genres:
        print(f"ID: {genre.codeganre} | Название: {genre.name}")

def add_genre():
    name = input("Введите название жанра: ").strip()
    while True:
        try:
            codeganre = int(input("Введите ID жанра (целое число): ").strip())
            existing = Ganre.get_genre_by_id(codeganre)
            if existing:
                print("Такой ID уже существует. Введите другой.")
            else:
                break
        except ValueError:
            print("Некорректный ввод. Введите целое число.")

    new_genre = Ganre(codeganre=codeganre, name=name)
    try:
        new_genre.save()
        print("Жанр успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении жанра: {e}")

def edit_genre():
    try:
        codeganre = int(input("Введите ID жанра для редактирования: ").strip())
    except ValueError:
        print("Некорректный ввод.")
        return
    genre = Ganre.get_genre_by_id(codeganre)
    if not genre:
        print("Жанр с таким ID не найден.")
        return
    print(f"Текущее название: {genre.name}")
    new_name = input("Введите новое название (оставьте пустым, чтобы не менять): ").strip()
    if new_name:
        genre.name = new_name
        try:
            genre.save()
            print("Жанр обновлен.")
        except Exception as e:
            print(f"Ошибка при обновлении: {e}")
    else:
        print("Изменения не внесены.")

def delete_genre():
    try:
        codeganre = int(input("Введите ID жанра для удаления: ").strip())
    except ValueError:
        print("Некорректный ввод.")
        return
    genre = Ganre.get_genre_by_id(codeganre)
    if not genre:
        print("Жанр с таким ID не найден.")
        return
    confirm = input(f"Вы уверены, что хотите удалить жанр '{genre.name}'? (да/нет): ").strip().lower()
    if confirm == 'да':
        try:
            genre.delete()
            print("Жанр удален.")
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
    else:
        print("Удаление отменено.")