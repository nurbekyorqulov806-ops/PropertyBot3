FROM python:3.10-slim

WORKDIR /app

# Kerakli tizim paketlarini o'rnatamiz
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt faylini nusxalaymiz
COPY requirements.txt .

# Kutubxonalarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Qolgan hamma fayllarni loyihaga nusxalaymiz
COPY . .

# Botni ishga tushirish buyrug'i (Faylingiz nomi property.py bo'lsa o'sha nomni yozing)
CMD ["python", "property.py"]