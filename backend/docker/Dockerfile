# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create logs directory
RUN mkdir -p /app/logs

# Create book_images directory
RUN mkdir -p /app/book_images

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run uvicorn when the container launches
CMD ["/bin/bash", "-c" , "cd src && uvicorn library.main:app --host 0.0.0.0 --port 8000 --reload"]
