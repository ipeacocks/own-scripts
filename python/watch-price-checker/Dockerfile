FROM python:3-alpine

WORKDIR /app

COPY . .
RUN apk add xvfb firefox
RUN pip install --no-cache-dir -r requirements.txt

# Xvfb is for Selenium
CMD ["sh", "-c", "nohup Xvfb :55 -screen 0 1024x768x16 & python3 -u main.py"]