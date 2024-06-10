import time
import csv
import aiohttp
import asyncio


async def send_data_to_fastapi(session, data):
    url = "http://127.0.0.1:8000/api/v1/add_queue"
    async with session.post(url, json=data) as response:
        if response.status == 200:
            print("Данные успешно отправлены!")
        else:
            print(f"Ошибка {response.status} при отправке данных.")


async def main():
    start = time.time()
    csv_file_path = "yappy_hackaton_2024_400k1.csv"

    async with aiohttp.ClientSession() as session:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            tasks = [send_data_to_fastapi(session, row) for row in csv_reader]
            await asyncio.gather(*tasks)

    print(time.time() - start)

if __name__ == "__main__":
    asyncio.run(main())
