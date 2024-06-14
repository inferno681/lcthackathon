import os
from openai import OpenAI
from ffmpeg.asyncio import FFmpeg
from uuid import uuid4
from ollama import AsyncClient
from ollama._types import Options
import requests
from uuid import uuid4
import random
import re


from services import config, convert_text_to_embeddings
PATH_TO_FILES = './temp/'
GPU_HOST = 'http://89.179.242.31'

ollama = AsyncClient(host=config.OLLAMA_SERVER)
options = Options(temperature=0.1, max_tokens=120)
# Объект подключения к серверу транскоибции аудиодорожки
client = OpenAI(api_key="cant-be-empty", base_url=f'{GPU_HOST}:8081/v1/')

# Задаем подключение к серверу эмбеддингов
embeddings = HuggingFaceHubEmbeddings(model=f'{GPU_HOST}:8082')

# Создаем объект подключения к серверу ollama, на котором поднята Llava
ollama = Client(host=f'{GPU_HOST}:8083')

# Устанавливаем температуру 0.1 для запросов к модели Llava
options = Options(temperature=0.1, max_tokens=120)

# Точка доступа к серверу переводов
TRANSLATE_HOST = f'{GPU_HOST}:8084/api/v1/translate'


async def add_video(link):
    # парсинг видеофайла, выделение аудиодорожки и первого кадра
    audio_file, face = await parse_video(link)

    # Транскрибция аудио
    text_from_audio = audio_transcribe(audio_file)
    os.remove(audio_file)

    # Формируем описание видео по первому кадру
    text_from_video = await image_recognition(face)

    # Переводим на русский язык, т.к. модель распознавания видео возвращает ответ на английском языке
    text_from_video = translate(text_from_video).strip('"')

    # Составление эмбеддингов, каждое предложение отдельный вектор эмбеддингов
    text_embed = []
    # Эмбеддинги аудиозаписи по предложениям
    if text_from_audio != '':
        for predl in text_from_audio.split("."):
            if (not str(predl.strip()).isdigit()) and (predl.strip() != ''):
                text_embed.append(await convert_text_to_embeddings(predl[:250]))

    # Эмбеддинги описаний видео по предложениям
    if text_from_video != '':
        for predl in text_from_video.split("."):
            if (not str(predl.strip()).isdigit()) and (predl.strip() != ''):
                text_embed.append(await convert_text_to_embeddings(predl[:250]))

    res = {
        'voise_description': text_from_audio,
        'image_description': text_from_video,
        'face': face,
        'embedding': text_embed,  # Массив эмбеддингов каждого предложения
    }

    # t_text = f'{text_from_audio} {text_from_video}'.strip()
    # if not t_text:
    #     t_text = "No sound"
    # embedding = await convert_text_to_embeddings(t_text)
    # res = {
    #     'voise_description': text_from_audio,
    #     'image_description': text_from_video,
    #     'full_description': t_text,
    #     'face': face,
    #     'embedding_description': embedding,
    # }
    return res


async def parse_video(link):
    out_audio = f'{PATH_TO_FILES}{uuid4()}.wav'
    out_face = f"{PATH_TO_FILES}{uuid4()}.png"

    ffmpeg = (
        FFmpeg()

        .option('y')
        .input(link)

        .output(out_audio,
                {"codec:a": "pcm_s16le"},
                vn=None,
                f="wav",)

        .output(out_face, vframes=1)
    )

    await ffmpeg.execute()
    return out_audio, out_face


def audio_transcribe(link):
    # Открываем файл аудиодорожки
    audio_file = open(link, 'rb')
    # Устанавливаем параметры расспознавания
    transcript = client.audio.transcriptions.create(
        model="Systran/faster-whisper-base",
        file=audio_file,
        temperature=0.0,
    )
    # Расспознаем аудиодорожку
    translated = transcript.text
    if len(translated) > 4:
        # Проверка языка расспознанного текста
        # Как правило язык не на русском означает фоновую музыку
        if bool(re.search('[а-яА-Я]', translated[5])):
            res = translated
        else:
            res = ''
    else:
        res = translated

    return res

# Функция описания видео по первому кадру


async def image_recognition(image_path):
    res = await ollama.generate(
        model='llava-llama3-int4',
        prompt='What is this a picture of shortly? Аnswer me briefly 1 main item.',
        images=[image_path],
        options=options,
        keep_alive=-1
    )
    return res['response']

# Функция перевода с английского на русский


async def translate(input_str):
    response = requests.post(TRANSLATE_HOST,
                             params={'input_str': input_str}
                             )
    if response:
        return response.content.decode('utf-8')
    else:
        return ''
