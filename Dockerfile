FROM python:3.12-slim
USER root
WORKDIR /bsp
#WORKDIR /usr/src/app/
RUN apt-get update
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
EXPOSE 5678
CMD ["python", "-m", "debugpy", "--wait-for-client", "--listen", "0.0.0.0:5678", "run.py"]