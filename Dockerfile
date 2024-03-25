# Use the official Python image as the base image
FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements/development.txt /app/requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --upgrade pip && \
   pip install -r /app/requirements.txt

# Copy the local code to the container
COPY . /app/

# Expose port 8000 for Django to use
EXPOSE 8000

# Command to run on container start
CMD ["python manage.py runserver 0.0.0.0:8000"]