from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from pprint import pprint  # Для красивого вывода

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["library"]
books = db["books"]


def add_book():
    print("\n--- Добавление книги ---")
    title = input("Название книги: ")
    author = input("Автор: ")
    year = int(input("Год издания: "))
    genres = input("Жанры (через запятую): ").split(",")

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genres": [genre.strip() for genre in genres],
        "is_available": True,
        "last_borrowed": None
    }

    result = books.insert_one(book)
    print(f"\n✅ Книга добавлена (ID: {result.inserted_id})")


def find_books():
    print("\n--- Поиск книг ---")
    query = input("Поиск (название/автор/жанр): ")
    results = books.find({
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"author": {"$regex": query, "$options": "i"}},
            {"genres": {"$in": [query.strip()]}}
        ]
    })

    print("\n🔍 Результаты поиска:")
    for book in results:
        status = "Доступна" if book.get("is_available", True) else "На руках"
        print(f"ID: {book['_id']}")
        print(f"Название: {book['title']}")
        print(f"Автор: {book['author']}")
        print(f"Год: {book['year']}")
        print(f"Жанры: {', '.join(book['genres'])}")
        print(f"Статус: {status}")
        print("-" * 30)


def list_all_books():
    print("\n--- Все книги в библиотеке ---")
    all_books = books.find().sort("title", 1)  # Сортировка по названию

    if books.count_documents({}) == 0:
        print("В библиотеке пока нет книг.")
        return

    for book in all_books:
        status = "🟢 Доступна" if book.get("is_available", True) else "🔴 На руках"
        last_borrowed = book.get("last_borrowed", "")
        if last_borrowed:
            last_borrowed = last_borrowed.strftime("%d.%m.%Y %H:%M")

        print(f"\n📖 {book['title']} ({book['year']})")
        print(f"👤 Автор: {book['author']}")
        print(f"🏷️ Жанры: {', '.join(book['genres'])}")
        print(f"📌 Статус: {status}")
        print(f"ID: {book['_id']}")
        if last_borrowed:
            print(f"⏳ Последний раз брали: {last_borrowed}")
            print(f"🆔 ID: {book['_id']}")


def update_book():
    print("\n--- Обновление книги ---")
    list_all_books()  # Показываем список для выбора
    book_id = input("\nВведите ID книги для обновления: ")

    try:
        book = books.find_one({"_id": ObjectId(book_id)})
        if not book:
            print("❌ Книга не найдена!")
            return

        print(f"\nТекущие данные книги '{book['title']}':")
        pprint(book)

        updates = {}
        print("\nВведите новые данные (оставьте пустым, если не меняется):")
        title = input("Название: ")
        if title: updates["title"] = title

        is_available = input("Доступна (y/n): ").lower()
        if is_available == "y":
            updates["is_available"] = True
            updates["last_borrowed"] = None
        elif is_available == "n":
            updates["is_available"] = False
            updates["last_borrowed"] = datetime.now()

        books.update_one({"_id": ObjectId(book_id)}, {"$set": updates})
        print("\n✅ Книга обновлена")
    except:
        print("❌ Ошибка: неверный формат ID")


def delete_book():
    print("\n--- Удаление книги ---")
    list_all_books()  # Показываем список для выбора
    book_id = input("\nВведите ID книги для удаления: ")

    try:
        result = books.delete_one({"_id": ObjectId(book_id)})
        if result.deleted_count > 0:
            print("\n✅ Книга удалена")
        else:
            print("❌ Книга не найдена!")
    except:
        print("❌ Ошибка: неверный формат ID")


def main():
    print("\n📚 Управление библиотекой (MongoDB)")
    while True:
        print("\n1. Добавить книгу")
        print("2. Найти книги")
        print("3. Показать все книги")
        print("4. Обновить книгу")
        print("5. Удалить книгу")
        print("6. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            find_books()
        elif choice == "3":
            list_all_books()
        elif choice == "4":
            update_book()
        elif choice == "5":
            delete_book()
        elif choice == "6":
            print("\nДо свидания! 👋")
            break
        else:
            print("❌ Неверный выбор")


if __name__ == "__main__":
    main()