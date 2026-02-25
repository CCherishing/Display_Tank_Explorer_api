FROM python:3.12-slim

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Fly typically routes traffic to internal port 8080
ENV PORT=8080
EXPOSE 8080

# Run gunicorn (production server)
# app:app means "from app.py import app"
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
