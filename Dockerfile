# Use official lightweight Python runtime as base image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy frontend code files into the container
COPY . .

# Install dependencies from requirements.txt without caching
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Command to run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
