[![Deploy](https://github.com/inferno681/lcthackathon/actions/workflows/deploy.yaml/badge.svg)](https://github.com/inferno681/lcthackathon/actions/workflows/deploy.yaml)
<br>

Документация к API доступна по url-адресу [SWAGER](https://lcthackathon.ddns.net/docs)

<details><summary><h1>Сервис загрузки и поиска видео</h1></summary>

* **MVP:**
  + Цель: Организация обработки и поиска видео.
  + Размещение: АПИ на сервере с ЦПУ, обработчик видео на сервере с ГПУ.

* **Функциональные возможности:**
  + Обработка видео по ссылке и внесение в информации о видео в базу данных.
  + Поиск видео различными алгоритмами.

* **Преимущества:**
  + Применение моделей машинного обучения для анализа видео.
  + Виды поиска: по тэгам, полнотекстовый, комбинированный.

</details>

<details><summary><h1>Инструкция по установке апи</h1></summary>

Клонируйте репозиторий и перейдите в него.
```bash
git@github.com:inferno681/lcthackathon.git
```

Для установки зависимостей создайте и активируйте виртульное окружение и выполните следующую команду:
```bash
pip install -r requirements.txt
```

Создайте файл **.env**, в корневой папке проекта, с переменными окружения.

```
APP_TITLE = Video search yappi (название сервиса для свагер)
APP_DESCRIPTION = Video search service (описание сервиса для свагер)
DB_HOST = localhost (хост базы данных)
DB_PORT = 5432 (порт базы данных)
POSTGRES_USER = postgres (имя пользователя для подключение к базе данных)
POSTGRES_PASSWORD = secret_password (пароль для подключения к базе данных)
POSTGRES_DB = postgres (название базы данных)
POOL_SIZE = 15 (количество одновременных соединений с базой данных)
POOL_TIMEOUT = 300 (таймаут для ответа апи)
EMBEDDINGS_SERVER = http://127.0.0.1:8082 (сервис эмбеддингов)
OLLAMA_SERVER = http://127.0.0.1:8083 (сервис оллама)
REDIS_HOST = localhost (хост редиса для загрузки задач)
REDIS_PORT = 6379 (порт редиса)

```

Находясь в корневой папке проекта выполните миграции.
  ```
  alembic upgrade head
  ```

Команда для запуска сервера:
  ```
  uvicorn app.main:app
  ```

</details>

<details><summary><h1>Запуск апи через докер</h1></summary>

- Клонируйте репозиторий.
- Перейдите в папку **infra** и создайте в ней файл **.env** с переменными окружения:
```
APP_TITLE = Video search yappi (название сервиса для свагер)
APP_DESCRIPTION = Video search service (описание сервиса для свагер)
DB_HOST = localhost (хост базы данных)
DB_PORT = 5432 (порт базы данных)
POSTGRES_USER = postgres (имя пользователя для подключение к базе данных)
POSTGRES_PASSWORD = secret_password (пароль для подключения к базе данных)
POSTGRES_DB = postgres (название базы данных)
POOL_SIZE = 15 (количество одновременных соединений с базой данных)
POOL_TIMEOUT = 300 (таймаут для ответа апи)
EMBEDDINGS_SERVER = http://127.0.0.1:8082 (сервис эмбеддингов)
OLLAMA_SERVER = http://127.0.0.1:8083 (сервис оллама)
REDIS_HOST = localhost (хост редиса для загрузки задач)
REDIS_PORT = 6379 (порт редиса)
```
- Из папки **infra** запустите docker-compose-api-prod.yaml:
  ```
  ~$ docker compose -f docker-compose-api-prod.yaml up -d
  ```
- В контейнере **backend** выполните миграции:
  ```
  ~$ docker compose -f docker-compose-api-prod.yaml exec backend alembic upgrade head

  ```

</details>

<details><summary><h1>Инструкция по установке обработчика</h1></summary>

Клонируйте репозиторий и перейдите в него.
```bash
git@github.com:inferno681/lcthackathon.git
```

Для установки зависимостей перейдите в папку "worker", создайте и активируйте виртульное окружение и выполните следующую команду:
```bash
pip install -r requirements.txt
```
Файл requirements.txt составлен с учет ГПУ NVIDIA. В случае применения других ГПУ этот файл необходимо изменить!

Создайте файл **.env**, в корневой папке проекта, с переменными окружения.

```
DB_HOST = (хост базы данных, подключенной к АПИ)
DB_PORT = (порт базы данных, подключенной к АПИ)
POSTGRES_USER = (имя пользователя базы данных, подключенной к АПИ)
POSTGRES_PASSWORD = (имя пользователя базы данных, подключенной к АПИ)
POSTGRES_DB = (название пользователя базы данных, подключенной к АПИ)
POOL_TIMEOUT = 300 (таймаут для ответа)
POOL_SIZE = 15 (количество одновременных соединений с базой данных)
EMBEDDINGS_HOST = (хост сервиса эмбеддингов)
WHISPER_HOST = (хост для сервера распознавания речи)
REDIS_HOST = (хост редис, подключенный к АПИ)
REDIS_PORT = (порт редис, подключенный к АПИ)
EMBEDDINGS_PORT = (порт сервиса эмбеддингов)
OLLAMA_HOST = (хост Оллама)
OLLAMA_PORT = (порт сервиса ОЛЛАМА)
OPENAI_PORT = (порт сервиса OPENAI)
TEMP_PATH = (путь к временным файлам)
MAX_JOBS = (количество одновременных задач)

```
Для сервиса оллама необходимо загрузить дополнительные модели:

```bash
# mmproj
wget https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf/resolve/main/llava-llama-3-8b-v1_1-mmproj-f16.gguf

# int4 llm
wget https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf/resolve/main/llava-llama-3-8b-v1_1-int4.gguf

# ollama int4 modelfile
wget https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf/resolve/main/OLLAMA_MODELFILE_INT4

docker run -d --gpus=all -v ./data:/root/.ollama -p 8083:11434 --name ollama ollama/ollama
```
В терминале заходим на контейнер ollama и выполняем команды:
```bash
ollama create llava-llama3-int4 -f ./OLLAMA_MODELFILE_INT4
ollama run llava-llama3-int4
```


Находясь в корневой папке проекта запустите обработчи очереди.
  ```
  arq main.WorkerSettings

  ```

</details>

<details><summary><h1>Запуск обработчика через докер</h1></summary>

- Клонируйте репозиторий.
- Перейдите в папку **infra** и создайте в ней файл **.env** с переменными окружения:
```
DB_HOST = (хост базы данных, подключенной к АПИ)
DB_PORT = (порт базы данных, подключенной к АПИ)
POSTGRES_USER = (имя пользователя базы данных, подключенной к АПИ)
POSTGRES_PASSWORD = (имя пользователя базы данных, подключенной к АПИ)
POSTGRES_DB = (название пользователя базы данных, подключенной к АПИ)
POOL_TIMEOUT = 300 (таймаут для ответа)
POOL_SIZE = 15 (количество одновременных соединений с базой данных)
EMBEDDINGS_HOST = (хост сервиса эмбеддингов)
WHISPER_HOST = (хост для сервера распознавания речи)
REDIS_HOST = (хост редис, подключенный к АПИ)
REDIS_PORT = (порт редис, подключенный к АПИ)
EMBEDDINGS_PORT = (порт сервиса эмбеддингов)
OLLAMA_HOST = (хост Оллама)
OLLAMA_PORT = (порт сервиса ОЛЛАМА)
OPENAI_PORT = (порт сервиса OPENAI)
TEMP_PATH = (путь к временным файлам)
MAX_JOBS = (количество одновременных задач)
```
- Из папки **infra** запустите docker-compose-worker-prod.yaml:
  ```
  ~$ docker compose -f docker-compose-worker-prod.yaml up -d
  ```
- Для загрузки и установки моделей Оллама запустите исполняемый файл:

  ```
  ~$ bash ollama.sh
  ```

</details>

<details><summary>Ссылки на используемые библиотеки</summary>

- [Python](https://www.python.org/downloads/release/python-3122/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [ARQ](https://arq-docs.helpmanual.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [PyTorch](https://pytorch.org/)
- [Ollama](https://www.ollama.com/)
- [Сервис эмбеддингов](https://huggingface.co/docs/text-embeddings-inference/index)

</details>

* **Разработчики Backend:**
  + [Василий](https://github.com/inferno681)
  + [Владимир](https://github.com/Vladimir-pro)

* **Разработчик Frontend:**
  + [Сергей](https://github.com/Tisavaco)
  + [Ссылка на репозиторий Frontend](https://github.com/Tisavaco/Hackathon.Web)
