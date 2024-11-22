FROM python:3.10-slim-buster

# Set non-interactive frontend for Debian-based systems
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    build-essential \
    libreoffice \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /usr/src/app

# Copy only necessary files (exclude unnecessary ones like tests, .git, etc.)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set the default command to run the Flask app
CMD ["python", "consumer.py"]
