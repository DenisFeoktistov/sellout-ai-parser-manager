# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install nano

# Copy the entire current directory into the container
COPY . .

# Expose the port on which your FastAPI application will run
EXPOSE 5000

# Command to run your FastAPI application
CMD ["python", "main.py"]
