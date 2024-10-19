# Use a base Python 3.9 image (or any version you prefer)
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into /app
COPY . /app

# Expose the port where the app will run (5000 is the default for Flask)
EXPOSE 5000

# Set necessary environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Run database migrations at the start (optional if you're using Flask-Migrate)
RUN flask db upgrade

# Command to run the Flask app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
