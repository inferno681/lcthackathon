import aiohttp
import aiofiles
import asyncio


async def send_file_to_fastapi(file_path, url):
    async with aiohttp.ClientSession() as session:
        try:
            async with aiofiles.open(file_path, 'rb') as file:
                form_data = aiohttp.FormData()
                form_data.add_field('file', file, filename=file_path)
                async with session.post(url, data=form_data) as response:
                    if response.status == 200:
                        print("Файл успешно отправлен!")
                    else:
                        print(f"Ошибка {response.status} при отправке файла.")
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except aiohttp.ClientError as e:
            print(f"Ошибка при выполнении HTTP запроса: {e}")

if __name__ == "__main__":
    asyncio.run(send_file_to_fastapi('./temp/fdab884f-7181-46ac-816e-a7203f601df1.png',
                'http://127.0.0.1:8000/api/v1/upload-image/'))
