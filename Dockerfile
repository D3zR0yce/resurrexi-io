FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py build.py ./
COPY templates/ templates/
COPY content/ content/
COPY static/ static/

# Build static site
RUN python3 build.py

# Expose port
EXPOSE 5000

# Run Flask app
CMD ["python3", "app.py"]
