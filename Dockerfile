FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg git curl ntpdate
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Install systemd-timesyncd for better time sync
RUN apt-get update && apt-get install -y systemd-timesyncd || true

CMD ["./start.sh"]
