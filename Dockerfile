# backend
FROM python:3.12-slim
USER root
WORKDIR /bsp
RUN apt-get update
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]

# frontend
# FROM node:alpine
# WORKDIR /bsp-frontend/usr/src/app
# COPY . /usr/src/app
# RUN npm install -g @angular/cli
# RUN npm install
# CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check", "--proxy-config", "proxy.conf.json"]

