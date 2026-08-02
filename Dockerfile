FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ src/

# Default port (Render automatically provides PORT env var)
ENV PORT=8000
EXPOSE ${PORT}

# Run the server using shell form to resolve $PORT dynamically
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]
