FROM python:3.13-slim

WORKDIR /app

# Install system dependencies (bash is included in python:3.13-slim)
# No additional packages needed for this application

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
EXPOSE 8509

# Note: Healthcheck is defined in docker-compose.yml for web service only
# CLI service doesn't need healthcheck

# Create a startup script
RUN echo '#!/bin/bash\n\
if [ "$MODE" = "web" ]; then\n\
    echo "Starting Web UI..."\n\
    streamlit run app.py --server.port=8509 --server.address=0.0.0.0\n\
else\n\
    echo "Starting CLI Version..."\n\
    python cli_app.py\n\
fi' > /app/start.sh && chmod +x /app/start.sh

# Set the entrypoint
ENTRYPOINT ["/app/start.sh"]