# 🎬 YaMDb: Платформа для оценки произведений

**YaMDb** — RESTful API для сбора отзывов и рейтингов произведений искусства.  
Пользователи взаимодействуют через JWT-аутентификацию, оставляя оценки (1-10) и текстовые рецензии. 

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


[Документация API](http://127.0.0.1:8000/redoc/)

### Примеры запросов и ответов: 

Регистрация нового пользователя (POST):
http://127.0.0.1:8000/api/v1/auth/signup/
````
Запрос в формате JSON:
{
"email": "user@example.com",
"username": "^w\\Z"
}

Ответ в формате JSON:

{
"email": "string",
"username": "string"
}
````
Получение JWT-токена (POST):
http://127.0.0.1:8000/api/v1/auth/token/
````
Запрос в формате JSON:
{
  "username": "^w\\Z",
  "confirmation_code": "string"
}

Ответ в формате JSON:

{
"token": "string"
}
````

Получение списка всех комментариев к отзыву (GET):
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
````
Ответ в формате JSON:

{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
````
Файлы хранятся в [api_yamdb/static/data](api_yamdb/static/data)

### 🛠 Технологии:
!Django 3.2(https://img.shields.io/badge/Django-3.2-092E20) 
!DRF 3.12(https://img.shields.io/badge/DRF-3.12-red) 
!JWT(https://img.shields.io/badge/Auth-JWT-green)

### <ins>Чтобы запустить проект, необходимо выполнить следующие шаги:</ins>

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
</details>
