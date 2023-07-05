FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY .. .

# Expose the Flask app port
EXPOSE 5000

# Set the entry point command to run the Flask app
CMD ["python", "app.py"]