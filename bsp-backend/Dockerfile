# backend
FROM python:3.12-slim
USER root
WORKDIR /bsp
RUN apt-get update
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "-u", "run.py"]