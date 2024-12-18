# Forbes parser

Forbes Parser — это инструмент для автоматизированного парсинга последних статей с сайта Forbes 
по новостным тегам.  

Для каждой статьи парсер собирает:
+ title - название
+ description - краткое описание
+ url - ссылка на статью
+ text - основной текст
+ publish_date - дата публикации

Теги для парсинга хранятся в файле `news_tags.py`.

Как добавить новый тег:
  1. Введите в браузере `Форбс + название темы`
  2. Откройте страницу
  3. Откройте консоль разработчика и перейдите во вкладку `network`
  4. Найдите нужную ссылку, домен которой начинается с `https://www.forbes.ru/api/`
  5. Добавьте название тега и ссылку на тег в файл `news_tags.py`

## Установка

1. Клонируйте репозиторий
  ```
  git clone <URL репозитория>
  cd forbes_parser
  ```

2. Установите зависимости:
  ```
  pip install -r requirements.txt
  ```

3. Настройте конфиг парсера в файле `config.py`
  + `MAX_RETRIES` - максимальное количество попыток отправки запроса, если при отправке возникла ошибка
  + `RETRY_DELAY` - время между повторными отправками запроса
  + `PARSING_INTERVAL` - периодичность сбора новостных статей


4. Добавьте прокси в файл `main.py`
Рекомендуется использовать прокси для снижение риска блокировки запросов от вашего IP адреса.


## Использование

Приложение может быть запущено в Docker контейнере или локально.

### Локальный запуск
1. Запустите парсер
  ```
  python3 app.py
  ```
2. Собранные статьи будут сохранены в файл `news_articles.json`

### Запуск в Docker
1. Соберите образ
  ```
  docker build -t forbes_parser .
  ```
  
2. Запустите контейнер
  ```
  docker run -d forbes_parser
  ```


## Комментарии
+ Вместо сохранения статей в json-файл вы можете добавить логику их добавления в базу данных
+ Слишком частый парсинг новостей может привести к блокировке IP адреса, поэтому используйте прокси