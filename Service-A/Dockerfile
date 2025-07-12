# Use official Python base image
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies needed by psycopg2 and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency metadata first to leverage Docker layer caching
COPY pyproject.toml ./

# Install project dependencies using pip
RUN pip install --upgrade pip && pip install .

# Copy the rest of the application code
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# TO BUILD:
# docker build -t lunchboxhub .

# TO RUN:
# docker run --env-file .env -p 8000:8000 --name my_lunch lunchboxhub