# Yamdb API

REST API для сбора отзывов на произведения искусства.

[Документация API](http://127.0.0.1:8000/redoc/)

## Основные возможности

🎬 **Произведения**

- Категории (Фильмы, Книги, Музыка)
- Жанры (Сказка, Рок, Артхаус)
- Рейтинг на основе пользовательских оценок

👥 **Пользователи**

- Трехуровневая система ролей (User, Moderator, Admin)
- JWT-аутентификация
- Регистрация через email-подтверждение

💬 **Отзывы и комментарии**

- Оценки от 1 до 10
- Один отзыв на произведение от пользователя
- Вложенные комментарии к отзывам

Разработчики

- Приложение Users [Андрей Олонцев]( https://github.com/Yoishiii)
- Приложение Titles [Саркар Ахмедов](https://github.com/Capkap)
- Приложение Reviews [Дарья Симашко](https://github.com/musthave-prog)

  <ins>Чтобы запустить проект, необходимо выполнить следующие шаги:</ins>

<details>

Создать виртуальное окружение:

````
python -m venv venv — для Windows.
python3 -m venv venv — для Mac и Linux.
````

Активировать виртуальное окружение:

````
source venv/Scripts/activate — для Windows.
source venv/bin/activate — для Mac и Linux.
````

Установить менеджер пакетов pip:

````
— python -m pip install --upgrade pip — для Windows.
— python3 -m pip install --upgrade pip — для Mac и Linux.
````

Установить все зависимости из файла requirements.txt:

````
— pip install -r requirements.txt — для Windows, Mac и Linux.
````

Чтобы запустить проект локально, используйте команду в терминале:

````
python manage.py runserver — для Windows, Mac и Linux.
````

Импорт данных из csv файлов:

````
python manage.py load_csv_data — для Windows, Mac и Linux.
````
Файлы хранятся в [api_yamdb/static/data](api_yamdb/static/data)
</details>
