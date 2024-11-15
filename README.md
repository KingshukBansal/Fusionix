# Fusionix - Video to MP3 Converter

**Fusionix** is a web application designed to convert videos into MP3 format. The application is built using **microservice architecture** and is aimed at practicing scalable, maintainable backend solutions. Each service is isolated and communicates via **RabbitMQ** for efficient message handling. The application is containerized using **Docker** and orchestrated using **Kubernetes**.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Service Architecture](#service-architecture)
4. [Usage](#usage)


---

## Project Overview

Fusionix provides a platform to convert videos into MP3 audio files. It is designed as a microservices-based application, where each service is dedicated to a specific functionality. The backend communicates using **RabbitMQ** for decoupling and scalability. Docker is used to containerize each service, and Kubernetes is used for orchestration.

### Features:
- User authentication (via the `auth` service)
- Video to MP3 conversion (via the `converter` service)
- Notification service to send messages when conversion is complete
- Gateway API for aggregating requests and routing them to appropriate services

---

## Technologies Used

- **Backend:**
  - **Python**: Used for the backend services.
  - **RabbitMQ**: Message broker for inter-service communication.
  - **Docker**: Containerization of services.
  - **Kubernetes**: Orchestration and management of containers.
  
- **Frontend:**
  - **React.js**: User interface for interaction with the application.
  - **Tailwind CSS**: Styling framework for the frontend.

---

## Service Architecture

The Fusionix application is divided into five core services, each with its own responsibility:

1. **Auth Service**: Handles user authentication and authorization.
2. **Gateway Service**: The entry point for all client requests, routing them to appropriate services.
3. **Converter Service**: Handles the core functionality of converting videos to MP3 format.
4. **Notification Service**: Sends notifications to users when their video conversion is complete.
5. **RabbitMQ**: A message broker facilitating communication between services.

Each service has its own isolated folder structure and communicates through RabbitMQ for scalability and asynchronous processing.

---

## Usage
After setting up both the frontend and backend:

1. Register a user using the registration form on the frontend.
2. Login to access the video-to-MP3 conversion functionality.
3. Upload a video and the backend will process the conversion asynchronously.
4. Receive notifications once the conversion is complete.