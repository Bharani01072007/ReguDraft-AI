FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for compilation and postgreSQL connections
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create local storage folders and configure correct permissions
RUN mkdir -p /app/storage_temp && chmod -R 777 /app/storage_temp

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
