FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install -r /app/Requirements.txt

CMD ["python3", "main.py"]
