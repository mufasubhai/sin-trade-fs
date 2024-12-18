# Use the official Python image from the Docker Hub
FROM python:3.12.4-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE ${PORT:-5004}

HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD curl --fail http://localhost:${PORT:-5004}  || exit 1

# Command to run the application
CMD sh -c "gunicorn src.app:app --bind 0.0.0.0:${PORT:-5004}"