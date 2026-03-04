FROM ubuntu:24.04
RUN apt-get update && apt-get install -y git python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/Dimillian/ACHNBrowserUI.git /app
WORKDIR /app
