# Use the official Python slim image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy and install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser

# Copy the rest of the application code
COPY . .

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Run with gunicorn instead of Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]