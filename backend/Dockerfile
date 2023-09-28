FROM python:3.11

WORKDIR /app/foodgram

RUN pip install gunicorn==20.1.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:9001", "foodgram.wsgi"]
