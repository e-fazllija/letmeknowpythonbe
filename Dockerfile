# Use Python 3.10
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies for Whisper (ffmpeg)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create models directory for Whisper models
RUN mkdir -p models

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]