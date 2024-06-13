import os
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from ffmpeg.asyncio import FFmpeg
from uuid import uuid4
from ollama import AsyncClient
from ollama._types import Options


from services import config, convert_text_to_embeddings
PATH_TO_FILES = './temp/'


ollama = AsyncClient(host=config.OLLAMA_SERVER)

options = Options(temperature=0.1, max_tokens=120)

device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32


model_id = "openai/whisper-base"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id,
    torch_dtype=torch_dtype,
    low_cpu_mem_usage=True,
    use_safetensors=True,
)
model.to(device)

processor_id = "openai/whisper-base"
processor = AutoProcessor.from_pretrained(processor_id)


pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    return_language=True,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)


async def add_video(link):

    audio_file, face = await parse_video(link)

    text_from_audio = audio_transcribe(audio_file)
    os.remove(audio_file)

    text_from_video = await image_recignition(face)
    print(text_from_video)
    t_text = f'{text_from_audio} {text_from_video}'.strip()
    if not t_text:
        t_text = "No sound"
    embedding = await convert_text_to_embeddings(t_text)
    res = {
        'voise_description': text_from_audio,
        'image_description': text_from_video,
        'full_description': t_text,
        'face': face,
        'embedding_description': embedding,
    }
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
    result = pipe(link, generate_kwargs={"task": "transcribe"})

    if result['chunks'][0]['language'] != 'russian':
        res = ''
    else:
        res = result['text']

    return res


async def image_recignition(image_path):
    res = await ollama.generate(
        model='llava-llama3-int4',
        prompt='What is this a picture of shortly? Аnswer me briefly 3 main items.',
        images=[image_path],
        options=options)
    return res['response']
