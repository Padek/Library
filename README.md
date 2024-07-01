**Library API
- This is a RESTful API for managing a library. The API supports CRUD operations for books, user authentication using JWT, and file upload/download for book covers. The application is built using FastAPI and MongoDB and is containerized using Docker.

**Features
- User Registration and Authentication (JWT)
- CRUD operations for Books and users
- File Upload and Download for Book Covers
- MongoDB for data storage
- Docker for containerization


**Prerequisites
- Docker and Docker Compose installed on your machine
- MongoDB Atlas account (or local MongoDB instance)
- Python 3.9 (for local development)


**Installation and Setup and Variables
- cd backend
- cmkdir -p data
- touch data/.env
- echo 'mongoDB_url = "mongodb+srv://admin:SecretPassword42@cluster0.b6mhx1i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"' > data/.env
- docker-compose up --build


**Clone the Repository
- git clone https://github.com/Padek/Library.git
