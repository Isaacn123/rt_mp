FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Upgrade pip first, then install requirements
# RUN pip install --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY cli_app.py .

# Create directory for configurations
RUN mkdir -p /app/configs

# Expose port for Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501/')"

# Create a startup script
RUN echo '#!/bin/bash\n\
if [ "$MODE" = "web" ]; then\n\
    echo "Starting Web UI..."\n\
    streamlit run app.py --server.port=8501 --server.address=0.0.0.0\n\
else\n\
    echo "Starting CLI Version..."\n\
    python cli_app.py\n\
fi' > /app/start.sh && chmod +x /app/start.sh

# Set the entrypoint
ENTRYPOINT ["/app/start.sh"]