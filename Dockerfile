# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Upgrade pip to the latest version to avoid installation issues
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Add a healthcheck to ensure Streamlit is running
HEALTHCHECK CMD streamlit hello

# Define the command to run your app
# Use --server.address=0.0.0.0 to make the app accessible from the host
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

