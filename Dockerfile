FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y vim

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
