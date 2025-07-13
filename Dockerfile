# Use the official Python image as a base
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libmariadb-dev && rm -rf /var/lib/apt/lists/*

# Install Poetry for dependency management
RUN pip install poetry

# Copy the project files
COPY pyproject.toml poetry.lock README.md /app/

# Copy the application code
COPY src/ /app/src/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "src.url_shortner.app:app", "--host", "0.0.0.0", "--port", "8000"]
