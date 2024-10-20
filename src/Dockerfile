FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --reload --port=8000 --host=0.0.0.0