FROM swift:5.9

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip git curl patch \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest pytest-timeout
COPY . .
