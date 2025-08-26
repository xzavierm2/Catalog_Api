
# Use Python base image
FROM  python:3.11-slim

# Set environment variables for Flask
ENV PYTHONUNBUFFERED=1
ENV PYTHDONTWRITEBYTECODE=1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0
ENV FLASK_ENV=development

# Set working directory inside container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install system dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app.py /app/app.py

# Copy requirements file if it exists
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir flask requests

# Expose the port the app runs on
EXPOSE 5050

# Ensure catalog_dta.json is present
RUN touch catalog_data.json

# Run the application
CMD ["flask", "run", "--host=0.0.0", "--port=5050"]


