# Library API

This is a RESTful API for managing a library. The API supports CRUD operations for books, user authentication using JWT, and file upload/download for book covers. The application is built using FastAPI and MongoDB and is containerized using Docker.

## Features

- User Registration and Authentication (JWT)
- CRUD operations for Books and users
- File Upload and Download for Book Covers
- MongoDB for data storage
- Docker for containerization

## Prerequisites

- Docker and Docker Compose installed on your machine
- MongoDB Atlas account (or local MongoDB instance)
- Python 3.9 (for local development)

## Installation and Setup and Variables
- cd backend
- cmkdir -p data (mac) OR mkdir -p data (on Windows)
- cd data
- touch data/.env (mac) OR New-Item -Path .env -ItemType File (on Windows)
- echo 'mongoDB_url = "mongodb+srv://admin:SecretPassword42@cluster0.b6mhx1i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"' > data/.env (mac)
    -- echo mongoDB_url = "mongodb+srv://admin:SecretPassword42@cluster0.b6mhx1i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" > .env (Windows)
- cd ..
- docker-compose up --build

### Clone the Repository
```bash
git clone https://github.com/Padek/Library.git
