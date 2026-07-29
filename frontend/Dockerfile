# Use official lightweight Python runtime as base image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy all files from frontend_files folder into container working directory
COPY . .

# Install Python dependencies from requirements.txt without caching to reduce image size
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose standard Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
