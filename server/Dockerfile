# Use the official Python image as a base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project files into the container
COPY . .

# Run the Django development server on container startup
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]