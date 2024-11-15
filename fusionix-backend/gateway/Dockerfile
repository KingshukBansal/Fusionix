FROM python:3.10-slim-bullseye

# Update and install necessary packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app

RUN pip install --no-cache-dir --requirement /app/requirements.txt


COPY . /app

EXPOSe 8080

CMD ["python", "server.py"]







