import time
import csv
import aiohttp
import asyncio

# Количество одновременных запросов
CONCURRENCY_LIMIT = 10
# Размер порции записей для отправки
BATCH_SIZE = 1000


async def send_data_to_fastapi(session, data):
    url = "http://lcthackathon.ddns.net:8000/api/v1/add_queue"
    async with session.post(url, json=data) as response:
        if response.status == 200:
            print("Данные успешно отправлены!")
        else:
            print(f"Ошибка {response.status} при отправке данных.")


async def process_chunk(session, chunk):
    tasks = [send_data_to_fastapi(session, row) for row in chunk]
    await asyncio.gather(*tasks)


async def main():
    start = time.time()
    csv_file_path = "yappy_hackaton_2024_400k.csv"
    chunk_size = 1000

    async with aiohttp.ClientSession() as session:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            chunk = []
            for row in csv_reader:
                chunk.append(row)
                if len(chunk) == chunk_size:
                    await process_chunk(session, chunk)
                    chunk = []
            if chunk:
                await process_chunk(session, chunk)

    print(f"Время выполнения: {time.time() - start} секунд")


if __name__ == "__main__":
    asyncio.run(main())
