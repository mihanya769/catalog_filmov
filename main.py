from flask import Flask, render_template
import random
from peewee import *
from generator import Film

# Подключаем базу данных
db = SqliteDatabase('films.db')

# Подключаем Flask
app = Flask(__name__)

# Маршрут для главной страницы
@app.route('/')
def start():
    # Извлекаем все фильмы из базы данных
    films = Film.select()

    # Формируем данные для передачи в шаблон
    film_title = []
    film_year = []
    film_runtime = []
    film_genre = []
    film_director = []
    film_pic_link = []
    for film in films:
        film_title.append(film.title)
        film_year.append(film.year)
        film_runtime.append(film.runtime)
        film_genre.append(film.genre)
        film_director.append(film.director)
        film_pic_link.append(film.pic_link)
    # Передаём данные в шаблон
    return render_template("main_page.html", main_data=zip(film_title,film_year,film_runtime, film_genre, film_director, film_pic_link))

# Запуск сервера Flask
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=random.randint(2000, 9000))

