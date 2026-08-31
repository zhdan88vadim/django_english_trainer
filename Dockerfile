FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

RUN apt-get update && apt-get install -y ffmpeg build-essential libsndfile1 && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install system dependencies including fonts
RUN apt-get update && apt-get install -y \
    fonts-dejavu \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /code/

RUN mkdir -p /tmp/video_generation

# Set permissions
RUN chmod -R 777 /tmp/video_generation

# Verify fonts are installed
RUN ls -la /usr/share/fonts/truetype/dejavu/