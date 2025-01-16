FROM --platform=linux/amd64 python:3.12-bookworm

ENV PYTHONUNBUFFERED 1

# Install Certificates CA
# RUN apt-get update && apt-get install -y ca-certificates && apt-get clean
# RUN update-ca-certificates

# RUN apt-get update && apt-get install -y curl && apt-get clean

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Eksponujemy port 8000
EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

CMD gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
