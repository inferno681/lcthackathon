import os
import re

import torch
from ffmpeg.asyncio import FFmpeg
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from ollama import AsyncClient
from ollama._types import Options
from openai import OpenAI
from transformers import MarianMTModel, MarianTokenizer
from uuid import uuid4


from services import config, convert_text_to_embeddings

TEMP_PATH = config.TEMP_PATH
if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)

# Объект подключения к серверу транскрибции аудиодорожки
openai_client = OpenAI(api_key="cant-be-empty", base_url=config.OPENAI_URL)

# Задаем подключение к серверу эмбеддингов
embeddings = HuggingFaceEndpointEmbeddings(model=config.EMBEDDINGS_URL)

# Создаем объект подключения к серверу ollama, на котором поднята Llava
ollama = AsyncClient(host=config.OLLAMA_URL)

# Устанавливаем температуру 0.1 для запросов к модели Llava
options = Options(temperature=0.1, max_tokens=120)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "Helsinki-NLP/opus-mt-en-ru"
model = MarianMTModel.from_pretrained(model_name).to(device)
tokenizer = MarianTokenizer.from_pretrained(model_name)


async def video_processing(link: str) -> dict:
    """Функция обработки видео"""
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
    if text_from_audio != "":
        for sentence in text_from_audio.split("."):
            if (not str(sentence.strip()).isdigit()) and (
                sentence.strip() != ""
            ):
                text_embed.append(
                    await convert_text_to_embeddings(sentence[:250])
                )

    # Эмбеддинги описаний видео по предложениям
    if text_from_video != "":
        for sentence in text_from_video.split("."):
            if (not str(sentence.strip()).isdigit()) and (
                sentence.strip() != ""
            ):
                text_embed.append(
                    await convert_text_to_embeddings(sentence[:250])
                )
    return {
        "voise_description": text_from_audio,
        "image_description": text_from_video,
        "face": face,
        "embedding": text_embed,  # Массив эмбеддингов каждого предложения
    }


async def parse_video(link: str):
    """Функция парсинга видео"""
    out_audio = f"{TEMP_PATH}{uuid4()}.wav"
    out_face = f"{TEMP_PATH}{uuid4()}.png"
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(link)
        .output(
            out_audio,
            {"codec:a": "pcm_s16le"},
            vn=None,
            f="wav",
        )
        .output(out_face, vframes=1)
    )
    await ffmpeg.execute()
    return out_audio, out_face


def audio_transcribe(link: str) -> str:
    """Функция транскрибирования аудиодорожки"""
    # Открываем файл аудиодорожки
    audio_file = open(link, "rb")
    # Устанавливаем параметры расспознавания
    transcript = openai_client.audio.transcriptions.create(
        model="Systran/faster-whisper-base",
        file=audio_file,
        temperature=0.0,
    )
    # Расспознаем аудиодорожку
    translated = transcript.text
    if len(translated) > 4:
        # Проверка языка расспознанного текста
        # Как правило язык не на русском означает фоновую музыку
        if bool(re.search("[а-яА-Я]", translated[5])):
            res = translated
        else:
            res = ""
    else:
        res = translated

    return res


async def image_recognition(image_path: str) -> str:
    """Функция описания видео по первому кадру"""
    return (
        await ollama.generate(
            model="llava-llama3-int4",
            prompt="What is this a picture of shortly? Аnswer me briefly 1 main item.",  # noqa
            images=[image_path],
            options=options,
            keep_alive=-1,
        )
    )["response"]


async def translate(input: str) -> str:
    result = []
    for str in input.split("."):
        if (not str.strip().isdigit()) and (str.strip() != ""):
            batch = tokenizer.prepare_seq2seq_batch(
                [str], return_tensors="pt"
            ).to(device)
            translation = model.generate(**batch)
            out = tokenizer.decode(translation[0], skip_special_tokens=True)
            result.append(out)
    if result:
        return ". ".join(result)
    else:
        return ""
