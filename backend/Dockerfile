# Use official lightweight Python runtime as base image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy all files from backend_files folder to container working directory
COPY . .

# Install Python dependencies from requirements.txt without caching to reduce image size
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Start application using Gunicorn server
# - `-w 4`: Uses 4 worker processes for concurrent handling
# - `-b 0.0.0.0:7860`: Binds server to port 7860 across all interfaces
# - `app:app`: References the Flask instance named 'app' defined in app.py
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:app"]
