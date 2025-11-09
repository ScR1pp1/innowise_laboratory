FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .  # <- Добавлена точка в конце!

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY startup.sh .
RUN chmod +x startup.sh

CMD ["python", "run.py"]