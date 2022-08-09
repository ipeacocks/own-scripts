FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        firefox \
        firefox-geckodriver \
        gpg-agent \
        xvfb \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# RUN add-apt-repository -y ppa:mozillateam/firefox-next && \
#     apt install -y firefox=104.0~b7+build1-0ubuntu0.22.04.1 && \
#     rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Xvfb is for Selenium
CMD ["sh", "-c", "nohup Xvfb :55 -screen 0 1024x768x16 & python3 -u main.py"]