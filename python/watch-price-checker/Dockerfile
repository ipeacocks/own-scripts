FROM python:3-alpine

WORKDIR /app

COPY . .
RUN apk --no-cache add xvfb firefox firefox-geckodriver libressl-dev libffi-dev python3-dev build-base gcc wget git 
RUN pip install --no-cache-dir -r requirements.txt

# Xvfb is for Selenium
CMD ["sh", "-c", "nohup Xvfb :55 -screen 0 1024x768x16 & python3 -u main.py"]