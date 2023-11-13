# RSS Scraper and Feed Management API

## Overview

This project is a simple RSS scraper and feed management API designed for a feed aggregator. The goal is to provide users with a backend service to save, view, and manage RSS feeds through a straightforward API. The service allows users to track their registered feeds, check the number of unread entries, and comment on individual feed items.

## Features

- **RSS Scraper:** Automatically fetch and save RSS feeds to MongoDB.
  
- **User Authentication:** Use PostgreSQL for user authentication.
  
- **Background Tasks:** Utilize Celery with RabbitMQ and Redis for handling background tasks.
  
- **Testing:** Use `mongomock` for writing tests with 97% coverage. Tests exclude specific modules using the `--omit` option.

- **Dockerized:** The application is containerized using Docker for easy deployment.

- **API Documentation:** A Postman collection is provided for API exploration.

## Technologies Used

- **Python:** The core language used for backend development.
  
- **Django:** A high-level web framework for building the API.
  
- **Django Rest Framework (DRF):** A powerful toolkit for building Web APIs on top of Django.
  
- **Database:** MongoDB for storing RSS feeds and PostgreSQL for user authentication.
  
- **Background Tasks:** Celery with RabbitMQ and Redis for handling asynchronous tasks.
  
- **Testing:** Mongomock for unit testing with 97% coverage.

- **Containerization:** Docker is used to containerize the application.

## Setup Instructions

## Setup Instructions

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/rss-scraper-api.git
    cd rss-scraper-api
    ```

2. **Set Up Environment Variables:**
    - Copy the `.env.example` file to a new file named `.env`.
    - Fill in the necessary environment variables in the `.env` file.
    ```bash
    cp .env.example .env
    # Edit .env to include your specific configurations
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Database Setup:**
    - Ensure your database services are running (e.g., MongoDB, PostgreSQL).
    - Run migrations: `python manage.py migrate`.

5. **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

6. **Using Docker (Optional):**
    - If you prefer using Docker, build and run the Docker container:
    ```bash
    docker-compose up --build
    ```

7. **Explore the API:**
    - Use the provided Postman collection for detailed information on available endpoints.

Happy coding! 🚀
