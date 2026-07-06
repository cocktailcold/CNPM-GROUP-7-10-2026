FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-tk tk \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_services.py"]
