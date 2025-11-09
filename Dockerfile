# 1. Base image (Python 3.10 slim version 사용)  
FROM python:3.10-slim

# 2. Install system dependencies including Chrome & ChromeDriver  
RUN apt-get update && apt-get install -y \
  wget \
  unzip \
  curl \
  gnupg \
  chromium \
  chromium-driver \
  --no-install-recommends && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# 3. Set environment variable for Chrome  
ENV DISPLAY=:99

# 4 Set working directory  
WORKDIR /app

# 5. Copy dependency list and install Python packages  
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code  
COPY . .

# 7. Expose port for app  
EXPOSE 5000

# 8. Run the Flask app using Gunicorn  
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-5000}"]