# 🤖 AI Assistant Telegram Bot

Telegram orqali foydalanuvchi savollarini qabul qilib, OpenAI GPT yordamida sun’iy intellekt javoblari qaytaruvchi asinxron Telegram bot.

---

## 📌 Loyihaning vazifasi

Ushbu loyiha MOBILE SOLUTIONS kompaniyasi uchun sinov loyihasi bo‘lib, `Django 5`, `FastAPI`, `Celery`, `Redis`, `PostgreSQL` kabi texnologiyalar yordamida yaratilgan. Telegram orqali kelgan xabarlar OpenAI API’ga yuboriladi va javob foydalanuvchiga qaytariladi.

---

## ⚙️ Texnologiyalar

- Python 3.11
- Django 5
- FastAPI
- python-telegram-bot==13.15 (sinxron versiya)
- Celery 5.5.2
- Redis
- PostgreSQL
- Pgbouncer
- OpenAI GPT (API orqali)
- Docker + Docker Compose
- Flower (Celery monitoring)
- Grafana + PostgreSQL monitoring

---

## 🛠 Loyihaning tuzilmasi

```
ai-gpt-bots-main/
├── bot/                # Telegram bot kodi
│   ├── handlers.py     # Xabarlar bilan ishlovchi funksiyalar
│   ├── webhook.py      # Webhook endpoint
│   └── tasks.py        # Asinxron Celery vazifalari
├── core/               # Django settings, celery config
│   ├── settings.py
│   ├── celery.py
│   └── urls.py
├── entrypoint.sh       # Docker start script
├── docker-compose.yml
├── Dockerfile
├── .env                # Maxfiy sozlamalar
└── README.md
```

---

## 🚀 O‘rnatish

### Talablar:

- Python 3.11+
- Redis
- PostgreSQL
- Docker (ixtiyoriy)

### 1. `.env` faylini sozlang

`.env` fayl quyidagicha bo‘lishi kerak:

```env
SECRET_KEY=...
DEBUG=1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=aiproject
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379

PROJECT_NAME=ai_gpt
WEB_PORT=8000

BOT_TOKEN="telegram-bot-token"
OPENAI_API_KEY="your-openai-key"
ASSISTANT_ID=""
DOMAIN="https://yourdomain.com"
```

### 2. Virtual muhit va paketlar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Migratsiyalar va superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Webhook o‘rnatish

```bash
python manage.py webhook
```

---

## 🧪 Ishlash jarayoni

1. Foydalanuvchi Telegram botga yozadi
2. `FastAPI` webhook bu xabarni qabul qiladi
3. Xabar `Celery` orqali `OpenAI API`ga yuboriladi
4. Javob Telegram orqali qaytariladi

---

## 🐳 Docker orqali ishga tushirish

```bash
docker-compose up --build -d
```

- `Flower`: http://localhost:5555
- `Backend`: http://localhost:8000

---

## 📊 Monitoring

- **Flower** – Celery ish holati kuzatuvi
- **Grafana** – PostgreSQL monitoring
- **pgbouncer** – Ulanishlar boshqaruvi

---

## ✉️ Muallif

**Ism**: Sherzamon  
**Telegram**: [@Sherzamon](https://t.me/Sherzamon_m)

---

