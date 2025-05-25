from models.book import get_all_books, get_book_by_code
from models.author import get_all_authors, get_author_by_id
from models.ganre import get_all_genres, get_genre_by_id


def menu_books():
    while True:
        print("\n=== 🎭 Книги 🎭 ===")
        print("1. 🧩 Показать все книги 🧩")
        print("2. 🎨 Добавить книгу 🎨")
        print("3. 🎬 Удалить книгу 🎬")
        print("4. 🎲 Изменить книгу 🎲")
        print("0. 🎪 Назад в главное меню 🎪")
        choice = input("🎰Выберите действие: ")
        if choice == "1":
            books = get_all_books()
            print("\nСписок книг:")
            for b in books:
                author = get_author_by_id(b.author_code)
                author_name = f"{author.name} {author.surname}" if author else "N/A"
                print(f"{b.codebook} | {b.name} | Автор: {author_name} | Цена: {b.price} руб.")
        elif choice == "2":
            print("\n=== Добавление новой книги ===")
            name = input("Название книги: ").strip()

            authors = get_all_authors()
            if not authors:
                print("Нет доступных авторов.")
                continue
            print("\nДоступные авторы (ID - Имя Фамилия):")
            for a in authors:
                print(f"{a.codeauthor} - {a.name} {a.surname}")
            try:
                author_code = int(input("Введите ID автора: "))
                if not any(a.codeauthor == author_code for a in authors):
                    print("Автор с таким ID не найден.")
                    continue
            except:
                print("Некорректный ID автора.")
                continue

            codeganre = select_genre()

            try:
                price = float(input("Цена: "))
            except:
                print("Некорректная цена.")
                continue

            from models.book import Book
            new_book = Book(
                codebook=None,
                name=name,
                author_code=author_code,
                price=price,
                codeganre=codeganre
            )
            new_book.save()
            print("✅ Книга добавлена.")
        elif choice == "3":
            codebook_input = input("Введите код книги для удаления: ").strip()
            try:
                codebook_to_delete = int(codebook_input)
            except:
                print("Некорректный код.")
                continue
            from models.book import get_book_by_code
            book_to_delete = get_book_by_code(codebook_to_delete)
            if book_to_delete:
                book_to_delete.delete()
                print("Книга удалена.")
            else:
                print("❌ Книга не найдена.")
        elif choice == "4":
            codebook_input = input("Введите код книги для редактирования: ").strip()
            try:
                codebook_to_edit = int(codebook_input)
            except:
                print("Некорректный код.")
                continue
            from models.book import get_book_by_code
            current_book = get_book_by_code(codebook_to_edit)
            if not current_book:
                print("❌ Книга не найдена.")
                continue
            new_name = input(f"Новое название ({current_book.name}): ").strip()

            current_author = get_author_by_id(current_book.author_code)
            current_author_name = f"{current_author.name} {current_author.surname}" if current_author else "N/A"
            print(f"\nТекущий автор: {current_author_name}")
            for a in get_all_authors():
                print(f"{a.codeauthor} - {a.name} {a.surname}")
            author_code_input = input("Введите новый ID автора (оставьте пустым): ").strip()

            from models.ganre import get_genre_by_id
            current_genre = get_genre_by_id(current_book.codeganre)
            current_genre_name = current_genre.name if current_genre else "N/A"
            print(f"\nТекущий жанр: {current_genre_name}")
            for g in get_all_genres():
                print(f"{g.codeganre} - {g.name}")
            codeganre_input = input("Введите новый ID жанра (оставьте пустым): ").strip()

            price_input = input(f"Новая цена ({current_book.price}): ").strip()

            new_name_final = new_name if new_name else current_book.name

            if author_code_input != "":
                try:
                    new_author_code = int(author_code_input)
                    if not any(a.codeauthor == new_author_code for a in get_all_authors()):
                        print("Автор с таким ID не найден.")
                        continue
                except:
                    print("Некорректный ID автора.")
                    continue
            else:
                new_author_code = current_book.author_code

            if codeganre_input != "":
                try:
                    new_codeganre = int(codeganre_input)
                    if not any(g.codeganre == new_codeganre for g in get_all_genres()):
                        print("Жанр с таким ID не найден.")
                        continue
                except:
                    print("Некорректный ID жанра.")
                    continue
            else:
                new_codeganre = current_book.codeganre

            if price_input != "":
                try:
                    new_price = float(price_input)
                except:
                    print("Некорректная цена.")
                    continue
            else:
                new_price = current_book.price

            from models.book import Book
            updated_book = Book(
                codebook=current_book.codebook,
                name=new_name_final,
                author_code=new_author_code,
                price=new_price,
                codeganre=new_codeganre
            )
            updated_book.save()
            print("✅ Книга обновлена.")
        elif choice == "0":
            break
        else:
            print("❌ Неверный ввод.")

def select_genre():
    genres = get_all_genres()
    print("\nДоступные жанры:")
    for g in genres:
        print(f"{g.codeganre}. {g.name}")
    while True:
        try:
            genre_choice = int(input("Выберите номер жанра из списка: "))
            genre = get_genre_by_id(genre_choice)
            if genre:
                return genre.codeganre
            else:
                print("Жанр с таким номером не найден. Попробуйте снова.")
        except:
            print("Некорректный ввод. Попробуйте снова.")