FROM python:3.10.6-slim-buster

ENV DHOMEDIR=/app

COPY . $DHOMEDIR/

WORKDIR $DHOMEDIR

# Update and install dependencies in one layer to prevent caching issues
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

CMD ["python", "./app.py"]