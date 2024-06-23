import time
import csv
import requests


def send_data_to_fastapi(session, data):
    url = "http://lcthackathon.ddns.net/:8000/api/v1/add_queue"
    response = session.post(url, json=data)
    if response.status_code == 200:
        print("Данные успешно отправлены!")
    else:
        print(f"Ошибка {response.status_code} при отправке данных.")


def main():
    start = time.time()
    csv_file_path = "yappy_hackaton_2024_400k.csv"

    with requests.Session() as session:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                send_data_to_fastapi(session, row)
                time.sleep(0.1)
    print(time.time() - start)


if __name__ == "__main__":
    main()
