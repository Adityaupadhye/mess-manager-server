# Use the official Python image from Docker Hub
FROM python:3.13.2-slim

# Set environment variables

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Copy the Django project files to the container
COPY . /app/

RUN python manage.py collectstatic --noinput

# Open the necessary port for Django
EXPOSE 8080

# Run the Django app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "api.wsgi:application"]
