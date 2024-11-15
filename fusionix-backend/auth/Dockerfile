FROM python:3.10-slim-bullseye

# Update and install necessary packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev\
    pkg-config \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app

# Install Python dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Copy the rest of the application
COPY . /app

EXPOSE 5000

# Run the app
CMD ["python", "server.py"]
