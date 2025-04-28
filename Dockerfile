# Use the official Python base image
FROM python:3.12.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements_rag_chat.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements_rag_chat.txt

# Copy the rest of the application code into the container
COPY rag_chat.py .
COPY common_utils.py .
COPY prompts.py .
COPY microsoft.png .
COPY .env .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "rag_chat.py", "--server.port=8501", "--server.address=0.0.0.0"]
