# Flask+Bash

## Запустить приложение

можно с помощью команды (Если установлен docker и docker compose)

```bash
bash up.sh
```
После этого произойдет следующее:
1. Поднимется контейнер с тестами
2. В нем выполнятся линт и тесты
3. Удалится контейнер с тестами
4. В случае успешного выполнения тестов, то поднимется контейнер с приложением

Документацию апи можно найти по адресу
```http://{host}:{port}/doc/swagger```

Например, при запуске с `bash up.sh` - ```http://localhost:8000/doc/swagger```


## Описание
Сервис позволяет выполнять популярные команды на Linux с помощью REST API

