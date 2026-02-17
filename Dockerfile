FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (sometimes needed for tokenizer libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .

# Install Python dependencies
# We use the CPU version of PyTorch to keep the image size reasonable
# Force torch 2.6.0 or newer
RUN pip install --no-cache-dir "torch>=2.6.0" --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]