# 🚀 EventPulse — Event Management API

**EventPulse** — bu online va offline tadbirlarni boshqarish uchun ishlab chiqilgan zamonaviy backend servis. Ushbu API orqali eventlar yaratish, foydalanuvchilarni ro‘yxatdan o‘tkazish va statistikalarni kuzatish mumkin.

---

## 🧰 Tech Stack

* **Backend:** Django 4.2 + Django REST Framework
* **Authentication:** SimpleJWT (Token-based auth)
* **Database:** PostgreSQL
* **Server:** Gunicorn
* **Reverse Proxy:** Nginx
* **Deployment:** AWS EC2 (Ubuntu 22.04)

---

## ⚙️ Local Setup

Quyidagi qadamlar orqali loyihani local muhitda ishga tushiring:

```bash
# Repository clone qilish
git clone https://github.com/yourusername/eventpulse.git
cd eventpulse

# Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependency o‘rnatish
pip install -r requirements.txt

# Environment fayl tayyorlash
cp .env.example .env
# .env faylni o‘zingizga moslab to‘ldiring

# Migrationlar
python manage.py makemigrations
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Serverni ishga tushirish
python manage.py runserver
```

---

## 🔐 Authentication

API **JWT (JSON Web Token)** orqali himoyalangan.

* Login qilgandan keyin sizga `access` va `refresh` token beriladi
* Protected endpointlar uchun header qo‘shing:

```http
Authorization: Bearer <your_access_token>
```

---

## 📌 API Endpoints

### 🔑 Authentication

| Method    | Endpoint                     | Description                   | Auth |
| --------- | ---------------------------- | ----------------------------- | ---- |
| POST      | `/api/auth/register/`        | Ro'yxatdan o'tish             | ❌    |
| POST      | `/api/auth/login/`           | Login (JWT olish)             | ❌    |
| POST      | `/api/auth/refresh/`         | Access token yangilash        | ❌    |
| GET / PUT | `/api/auth/profile/`         | Profilni ko‘rish / tahrirlash | ✅    |
| POST      | `/api/auth/change-password/` | Parolni o‘zgartirish          | ✅    |

---

### 🎯 Events

| Method      | Endpoint            | Description        | Auth     |
| ----------- | ------------------- | ------------------ | -------- |
| GET         | `/api/events/`      | Eventlar ro‘yxati  | ✅        |
| POST        | `/api/events/`      | Event yaratish     | 🔒 Admin |
| GET         | `/api/events/{id}/` | Event detail       | ✅        |
| PUT / PATCH | `/api/events/{id}/` | Eventni tahrirlash | 🔒 Admin |
| DELETE      | `/api/events/{id}/` | Eventni o‘chirish  | 🔒 Admin |

---

### 👥 Registrations

| Method | Endpoint                          | Description                         | Auth |
| ------ | --------------------------------- | ----------------------------------- | ---- |
| GET    | `/api/registrations/`             | Foydalanuvchining registratsiyalari | ✅    |
| POST   | `/api/registrations/`             | Eventga yozilish                    | ✅    |
| POST   | `/api/registrations/{id}/cancel/` | Registratsiyani bekor qilish        | ✅    |

---

### 📊 Event Qo‘shimcha Endpointlar

| Method | Endpoint                         | Description           | Auth |
| ------ | -------------------------------- | --------------------- | ---- |
| GET    | `/api/events/{id}/participants/` | Event ishtirokchilari | ✅    |
| GET    | `/api/events/{id}/stats/`        | Event statistikasi    | ✅    |

---

### 📈 Statistikalar

| Method | Endpoint                      | Description            | Auth     |
| ------ | ----------------------------- | ---------------------- | -------- |
| GET    | `/api/statistics/top-events/` | Eng mashhur 5 event    | ✅        |
| GET    | `/api/admin/statistics/`      | Admin statistik paneli | 🔒 Admin |

---

## 🧠 Business Logic (Muhim Qoidalar)

* Foydalanuvchi **bitta eventga faqat 1 marta** yozila oladi
* Event capacity (sig‘im) oshib ketmaydi
* `capacity = 0` → registratsiya yopiq
* `end_time < start_time` → validation error

---

## 🔒 Security

* `DEBUG=False` productionda
* `.env` fayl repositoryga qo‘shilmaydi
* `ALLOWED_HOSTS` sozlangan
* JWT authentication ishlatiladi

---

## 🌍 Deployment

Project production muhitda quyidagicha ishlaydi:

* Gunicorn → Django appni ishga tushiradi
* Nginx → reverse proxy + static files serve qiladi
* AWS EC2 → hosting server

---

## 📌 Xulosa

EventPulse — bu real biznes logikaga ega, production-ready backend loyiha bo‘lib, quyidagilarni o‘z ichiga oladi:

* 🔐 Secure authentication
* 🎯 Event management
* 👥 Registration system
* 📊 Real-time statistics
* 🚀 Production deployment

---

Agar sizda savollar bo‘lsa yoki contribution qilmoqchi bo‘lsangiz — bemalol murojaat qiling 🙂
