FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

WORKDIR /app

COPY requirements_docker.txt ./

RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y vim

RUN pip install -r requirements_docker.txt --no-cache-dir

COPY . .

CMD ["arq", "main.WorkerSettings"]
