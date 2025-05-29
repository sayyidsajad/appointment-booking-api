
# Appointment Booking System

A lightweight full-stack appointment booking system built with:

- A plug-and-play frontend booking widget
- A Flask REST API backend with SQLite
- Real-time slot availability
- 30-minute slots between 10 AM – 5 PM (lunch break 1–2 PM)
- Clean and modular architecture

---

## Project Structure

```
appointment-booking/
├── backend/
│   ├── app.py               # Flask application
│   ├── models.py            # SQLAlchemy models
│   ├── requirements.txt     # Python dependencies
│   ├── test_app.py          # Unit tests
│   └── .env                 # Environment variables
└── README.md
```

---

## Backend Setup (Flask)

### 1. Clone & Setup

```bash
git clone https://github.com/sayyidsajad/appointment-booking-api.git
cd appointment-booking-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Create `.env` file

```env
SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=secret_flask_key
FLASK_ENV=development
```

> The database file will be created automatically on first run.

### 3. Run the server

```bash
python app.py
```

> Access the API at: `http://127.0.0.1:5000`

---

## API Endpoints

### `GET /api/available-slots?date=YYYY-MM-DD`

Returns available 30-minute time slots for a specific date.

```bash
curl http://127.0.0.1:5000/api/available-slots?date=2024-06-01
```

---

### `POST /api/book`

Books a given slot (if not already booked).

**Payload:**

```json
{
  "name": "John Doe",
  "phone": "9876543210",
  "date": "2024-06-01",
  "time_slot": "10:00"
}
```

---
