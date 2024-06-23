import time
import csv
import aiohttp
import asyncio

# Количество одновременных запросов
CONCURRENCY_LIMIT = 10
# Размер порции записей для отправки
BATCH_SIZE = 1000


async def send_data_to_fastapi(session, data):
    url = "http://127.0.0.1:8000/api/v1/add_queue"
    try:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                print("Данные успешно отправлены!")
            else:
                print(f"Ошибка {response.status} при отправке данных: {
                      response.status}")
    except Exception as e:
        print(f"Ошибка при отправке данных: {e}")


async def worker(semaphore, session, batch):
    async with semaphore:
        await send_data_to_fastapi(session, batch)


async def main():
    start = time.time()
    csv_file_path = "yappy_hackaton_2024_400k.csv"
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    async with aiohttp.ClientSession() as session:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            batch = []
            tasks = []

            for row in csv_reader:
                batch.append(row)
                if len(batch) == BATCH_SIZE:
                    task = worker(semaphore, session, batch)
                    tasks.append(task)
                    batch = []  # Очистить текущую партию

                # Если количество задач достигает лимита параллелизма, подождать их завершения
                if len(tasks) >= CONCURRENCY_LIMIT:
                    await asyncio.gather(*tasks)
                    tasks = []

            # Отправить оставшиеся записи в последней неполной партии
            if batch:
                task = worker(semaphore, session, batch)
                tasks.append(task)

            # Подождать завершения всех задач
            await asyncio.gather(*tasks)

    print(f"Время выполнения: {time.time() - start} секунд")

if __name__ == "__main__":
    asyncio.run(main())
