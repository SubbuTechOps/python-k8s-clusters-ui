FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy frontend files
COPY frontend/ /app/frontend/

# Install a simple HTTP server for frontend
RUN pip install --no-cache-dir http-server

# Expose ports for API and frontend
EXPOSE 5000 8080

# Start both services
CMD ["sh", "-c", "python app.py & cd frontend && python -m http.server 8080"]
