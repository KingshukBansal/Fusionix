# Use the official Python 3.9 image from Docker Hub as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file (if you have one) to the container's working directory
COPY requirements.txt /app/

# Install the dependencies listed in the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container's working directory
COPY . /app/

# Expose port 5000, the default port for Flask
EXPOSE 8080

# Run the Flask app when the container starts
CMD ["python", "server.py"]
