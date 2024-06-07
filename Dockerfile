FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install -r /app/Requirements.txt

ARG GIT_COMMIT=unspecified
LABEL org.opencontainers.image.revision=$GIT_COMMIT

CMD ["python3", "main.py"]
