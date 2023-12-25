# За нами следят

<p align="center">
    <img src="https://img.shields.io/badge/python-v3.12+-blue.svg">
    <img src="https://img.shields.io/github/issues/evilyach/we-are-being-watched.svg">
    <img src="https://img.shields.io/badge/contributions-welcome-orange.svg">
<p>

<p align="center">
    <b>"За нами следят"</b> - тестовое задание по реализации веб-сервиса для учета посещенных ресурсов.
</p>

* С помощью POST-запроса можно зарегистрировать посещение ресурсов.
* С помощью GET-запроса можно посмотреть зарегистрированные посещения, включая
фильтрацию под дате.
* Более подробную документацию см. по http://localhost:8080/docs.

## Установка

Запустите контейнер.

```bash
docker compose up --build
```

При первом запуске необходимо инициализировать базу данных.

```bash
docker compose exec app alembic upgrade head
```

## Тестирование

Для запуска тестов с запущенным контейнером:

```bash
docker compose exec app pytest -v
```