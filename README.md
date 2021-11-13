# Бот-анализатор отзывов

> Для хакатона Wildhack, ноябрь 2021

## Локальная сборка

1. Переменные окружения должны лежать в `src/app/.env`, можно взять за основу `src/app/.env.default`. Нужно их обновить перед первой сборкой
2. Запустить локально ngrok командой `hngrok http 80`, выданный адрес записать в `src/app/.env`
2. `docker compose build`
3. `docker compose up`
4. Зайти в контейнер `web` (например, командой `docker compose exec web`) и в нем выполнить следующие команды:
    * `python3 manage.py migrate` 
    * `python3 manage.py reset_webhook`
    * Опционально можно создать себе суперпользователя для входа в Django Admin командой `python3 manage.py createsuperuser`


## Локальный запуск

1. Не забыть запустить и обновить в `src/app/.env` адрес ngrok
2. `docker compose up`
3. Если ngrok адрес менялся, зайти в контейнер `web` и запустить `python3 manage.py reset_webhook`


## CI/CD

1. Деплой средствами Github Actions на Heroku, конфигурация в папке `.github`

## Структура репозитория

1. Django апликейшн один, называется `app`
2. Настройки разбиты с помощью `django-split-settings`, ссылки на конфигурации в `src/app/settings.py`, сами конфигурации в `src/app/conf/*`. Можно не стеснятсья добавлять файлы.
3. Механика работы бота описана в `src/app/bot.py`
4. Таблица для джанго пользователей – `app_user`, для те – `app_telegram_user`. Между собой они не связаны.

## Управление

Стандартная Django admin по адресу `http://localhost/admin`