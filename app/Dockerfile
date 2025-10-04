# ingester/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy everything in the current directory to /app in the container
COPY . /app

# Install minimal deps for vectorizing & pushing to Qdrant
RUN pip install --upgrade pip && pip install -r requirements.txt

## Default envs (overridden by docker-compose)
#ENV QDRANT_URL=http://qdrant:6333\
#    COLLECTION_NAME=documents

# Run the one-shot ingestion script and exit
# Make sure your script path matches this command.
#RUN python3 history_tabs.py
CMD ["streamlit", "run", "app.py" , "--server.port=8501", "--server.address=0.0.0.0"]
