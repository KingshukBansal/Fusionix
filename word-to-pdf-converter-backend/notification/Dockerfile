# Use Python 3.10 slim-bullseye as the base image
FROM python:3.10-slim-bullseye

# Update and install necessary packages
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
  && rm -rf /var/lib/apt/lists/*  # Clean up the apt cache to reduce image size

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY ./requirements.txt /app/

# Install the Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Define the command to run the consumer.py script
CMD ["python", "consumer.py"]
