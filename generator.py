import os
import requests
from peewee import *

# Настройка подключения к базе данных
db = SqliteDatabase('films.db')

class Film(Model):
    title = CharField()
    year = IntegerField()
    runtime = CharField()
    genre = CharField()
    director = CharField()
    pic_link = CharField()
    class Meta:
        database = db
        db_table = 'films'

# Функция для добавления фильма в базу данных
def add_film(arg):
    # Создаем таблицу, если её нет
    db.connect()
    db.create_tables([Film])

    # Запрос к API для получения данных о фильме
    response = requests.get(f"http://www.omdbapi.com/?t={arg}&apikey=617499c0")
    r = response.json()

    # Скачивание и сохранение постера фильма
    img_data = requests.get(r["Poster"]).content
    poster_path = f'static//{arg}.jpg'

    # Создаем директорию static, если её нет
    os.makedirs('static', exist_ok=True)

    with open(poster_path, 'wb') as h:
        h.write(img_data)
    poster_path = f'{arg}.jpg'
    # Сохраняем данные о фильме в базе данных
    film = Film.create(
        title=r["Title"],
        year=int(r["Year"]),
        runtime=r["Runtime"],
        genre=r["Genre"],
        director=r["Director"],
        pic_link=poster_path
    )

    print(f"Фильм '{film.title}' добавлен в базу данных.")
    # Закрываем подключение к базе данных
    db.close()

def deduplicate_films():
    db.connect()
    query = (Film
             .select(Film.title,Film.year)
             .group_by(Film.title,Film.year)
             .having(fn.COUNT(Film.id)>1))
    # Для каждого набора дубликатов оставляем одну запись, остальные удаляем
    for film in query:
        duplicates = (Film
                      .select()
                      .where((Film.title == film.title) & (Film.year == film.year))
                      .order_by(Film.id))

        # Оставляем только один экземпляр (первую запись), остальные удаляем
        first_film = duplicates[0]  # Оставляем первый фильм
        for duplicate in duplicates[1:]:
            duplicate.delete_instance()  # Удаляем остальные

        print(f"Дубликаты для фильма '{first_film.title}' ({first_film.year}) удалены.")
    db.close()

if __name__ == '__main__':
    # Пример использования функции для добавления фильма
    add_film('Oppenheimer')
    deduplicate_films()

