# Use Python 3.10
FROM python:3.10

# Set working directory
WORKDIR /app

# Configure Whisper storage and startup preload inside the container
ENV WHISPER_MODELS_DIR=/app/models
ENV WHISPER_PRELOAD_MODEL=turbo

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

# Download the Whisper model during the image build so runtime requests do not block on it.
ARG PRELOAD_WHISPER_MODEL=turbo
RUN mkdir -p "$WHISPER_MODELS_DIR"
RUN if [ -n "$PRELOAD_WHISPER_MODEL" ]; then python -c "import whisper; whisper.load_model('$PRELOAD_WHISPER_MODEL', device='cpu', download_root='$WHISPER_MODELS_DIR')"; fi

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
