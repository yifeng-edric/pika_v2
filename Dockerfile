# The base image is correct for a Python 3.10 application.
FROM python:3.10-slim

# Setting PYTHONUNBUFFERED to 1 is correct, it ensures that Python output is unbuffered.
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container to /app.
WORKDIR /app

# Copy the requirements.txt file into the container at /app.
COPY requirements.txt .

# Install the Python dependencies specified in requirements.txt.
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app.
COPY . .

# Inform Docker that the container listens on the specified api_client port at runtime.
EXPOSE 3460
EXPOSE 9580
EXPOSE 8082

# Specify the command to run the application.
CMD ["python", "main.py"]
