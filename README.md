# Log Parser

Скрипт читает один или несколько лог-файлов в указанной папке, извлекает статистику по запросам и сохраняет результат в JSON.

## Возможности
- 
- Обработка лог-файла одного или нескольких в указанной директории.
- Подсчёт общего количества запросов.
- Подсчёт запросов по методам: `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`, `HEAD`.
- Поиск топ-3 IP-адресов по количеству запросов.
- Поиск топ-3 самых долгих запросов.
- Сохранение статистики в отдельный JSON-файл для каждого лога.
- Вывод статистики в терминал.


## Запуск

Обработка одного файла:

```bash
python log_parser.py -f ./access.log
```

Обработка всех `.log`-файлов в директории:

```bash
python log_parser.py -f logs
```

Пример вывода:

```text
Файл: ./access.log
Общее количество запросов: 3216723
Количество запросов по HTTP-методам:
GET - 2247848
POST - 918794
PUT - 70
DELETE - 1
OPTIONS - 39
HEAD - 49971
Топ 3 IP адресов:
193.106.31.130 - 235209
198.50.156.189 - 167812
5.112.235.245 - 166722
Топ 3 самых долгих запросов:
POST /administrator/index.php IP: 62.93.172.245 длительность: 10000 мс дата: [23/Dec/2015:07:27:57 +0100]
GET /media/system/css/modal.css IP: 213.162.68.113 длительность: 10000 мс дата: [06/Jan/2016:18:47:57 +0100]
GET /images/phocagallery/almhuette/thumbs/phoca_thumb_m_terasse.jpg IP: 194.166.55.43 длительность: 10000 мс дата: [06/Jan/2016:21:29:02 +0100]
Статистика сохранена в файл: .\access_result.json
```
## Результат

Для файла `access.log` будет создан файл `access_result.json`.

Пример структуры JSON:

```json
{
    "top_ips": {
        "193.106.31.130": {
            "GET": 18709,
            "POST": 216500,
            "PUT": 0,
            "DELETE": 0,
            "OPTIONS": 0,
            "HEAD": 0
        },
        "198.50.156.189": {
            "GET": 2,
            "POST": 167810,
            "PUT": 0,
            "DELETE": 0,
            "OPTIONS": 0,
            "HEAD": 0
        },
        "5.112.235.245": {
            "GET": 166722,
            "POST": 0,
            "PUT": 0,
            "DELETE": 0,
            "OPTIONS": 0,
            "HEAD": 0
        }
    },
    "top_longest": [
        {
            "ip": "62.93.172.245",
            "date": "[23/Dec/2015:07:27:57 +0100]",
            "method": "POST",
            "url": "/administrator/index.php",
            "duration": 10000
        },
        {
            "ip": "213.162.68.113",
            "date": "[06/Jan/2016:18:47:57 +0100]",
            "method": "GET",
            "url": "/media/system/css/modal.css",
            "duration": 10000
        },
        {
            "ip": "194.166.55.43",
            "date": "[06/Jan/2016:21:29:02 +0100]",
            "method": "GET",
            "url": "/images/phocagallery/almhuette/thumbs/phoca_thumb_m_terasse.jpg",
            "duration": 10000
        }
    ],
    "total_stat": {
        "GET": 2247848,
        "POST": 918794,
        "PUT": 70,
        "DELETE": 1,
        "OPTIONS": 39,
        "HEAD": 49971
    },
    "total_requests": 3216723
}
```