FROM python:3.12-alpine

# Install system dependencies
RUN apk add --no-cache \
    libpq-dev gcc musl-dev python3-dev postgresql-dev

# Set the working directory in the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]