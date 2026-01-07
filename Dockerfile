FROM python:3.11-slim

# Install kcat dependencies
RUN apt-get update && apt-get install -y \
    kafkacat \
    librdkafka-dev \
    nano \
    curl \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# Install pip dependencies
RUN pip install --no-cache-dir requests confluent-kafka kafka-python

# Copy your script
COPY producer.py /scripts/producer.py
COPY producer2.py /scripts/producer2.py
COPY consumer.py /scripts/consumer.py

WORKDIR /scripts
CMD ["sleep", "infinity"]
