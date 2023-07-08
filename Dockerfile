# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the Flask application port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
