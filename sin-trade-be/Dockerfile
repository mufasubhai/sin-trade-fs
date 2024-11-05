# Use the official Python image from the Docker Hub
FROM python:3.12.4-slim

# Set the working directory
WORKDIR /app

# Install the dependencies
RUN pip install --no-cache-dir pipenv

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock ./

# Install the dependencies using pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE ${PORT:-5002}

HEALTHCHECK --interval=5s --timeout=3s --retries=3 CMD curl --fail http://localhost:$PORT || exit 1

# Command to run the application
CMD sh -c "pipenv run gunicorn src.app:app --bind 0.0.0.0:${PORT:-5002}"