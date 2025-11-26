# 🏋️ Service Membership API

> A robust backend system for managing members, plans, subscriptions, and attendance check-ins for services like Gyms, Coaching Centers, or Salons.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a393?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?style=flat&logo=postgresql)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat&logo=python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red?style=flat)](https://www.sqlalchemy.org/)

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Database Schema](#-database-schema)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

---

## ✨ Features

- **Member Management** - Complete CRUD operations for member profiles
- **Flexible Plans** - Create and manage subscription plans with custom durations
- **Smart Subscriptions** - Automatic end date calculation based on plan duration
- **Attendance Tracking** - Real-time check-in system with database triggers
- **Auto-Update Counters** - PostgreSQL triggers automatically maintain check-in counts
- **Interactive API Docs** - Built-in Swagger UI for testing endpoints
- **Search & Filter** - Query members by status, name, or other criteria
- **Clean Architecture** - Modular design with separate routers and schemas
- **Type Safety** - Pydantic schemas for request/response validation
- **Unit Testing** - Pytest integration with example tests

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Language** | Python 3.10+ | Core programming language |
| **Framework** | FastAPI | High-performance web framework |
| **Database** | PostgreSQL | Relational database with triggers |
| **ORM** | SQLAlchemy 2.0 | Database abstraction layer |
| **Validation** | Pydantic | Data validation and serialization |
| **API Docs** | Swagger/OpenAPI | Auto-generated documentation |
| **Testing** | Pytest | Unit and integration testing |
| **Environment** | python-dotenv | Configuration management |

---

## 📁 Project Structure

```
membership-api/
├── 📄 README.md                 # Project documentation
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Environment variables (create this)
├── 📄 triggers.sql              # PostgreSQL trigger definitions
├── 📄 test_main.py              # Unit tests
│
└── app/
    ├── 📄 __init__.py
    ├── 📄 main.py               # FastAPI application entry point
    ├── 📄 database.py           # Database connection and session
    ├── 📄 models.py             # SQLAlchemy ORM models
    ├── 📄 schemas.py            # Pydantic schemas
    │
    └── routers/
        ├── 📄 __init__.py
        ├── 📄 members.py        # Member endpoints
        ├── 📄 plans.py          # Plan endpoints
        ├── 📄 subscriptions.py  # Subscription endpoints
        └── 📄 attendance.py     # Attendance endpoints
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 13 or higher
- pip (Python package manager)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/membership-api.git
cd membership-api
```

#### 2. Create Virtual Environment

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/membership_db

# Optional: API Configuration
API_TITLE=Service Membership API
API_VERSION=1.0.0
```

> **Note:** Replace `YOUR_PASSWORD` with your PostgreSQL password.

#### 5. Create Database

Open PostgreSQL (pgAdmin or psql shell) and run:

```sql
CREATE DATABASE membership_db;
```

#### 6. Start the Application

```bash
uvicorn app.main:app --reload
```

The application will:
- Start on `http://127.0.0.1:8000`
- Automatically create database tables
- Generate API documentation

#### 7. Apply PostgreSQL Trigger

Open `triggers.sql` in pgAdmin Query Tool and execute:

```sql
DROP TRIGGER IF EXISTS trg_update_checkin_count ON attendance;
DROP FUNCTION IF EXISTS update_checkin_count;

CREATE OR REPLACE FUNCTION update_checkin_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE members
    SET total_check_ins = total_check_ins + 1
    WHERE id = NEW.member_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_checkin_count
AFTER INSERT ON attendance
FOR EACH ROW
EXECUTE FUNCTION update_checkin_count();
```

---

## 🗄️ Database Schema

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Member    │         │  Subscription    │         │    Plan     │
├─────────────┤         ├──────────────────┤         ├─────────────┤
│ id (PK)     │────┐    │ id (PK)          │    ┌────│ id (PK)     │
│ name        │    │    │ member_id (FK)   │────┘    │ name        │
│ phone       │    │    │ plan_id (FK)     │         │ price       │
│ status      │    │    │ start_date       │         │ duration_days│
│ total_check_ins│ │    │ end_date         │         │ created_at  │
│ created_at  │    │    │ created_at       │         └─────────────┘
└─────────────┘    │    └──────────────────┘
                   │
                   │    ┌──────────────────┐
                   └────│   Attendance     │
                        ├──────────────────┤
                        │ id (PK)          │
                        │ member_id (FK)   │
                        │ check_in_time    │
                        └──────────────────┘
```

**Relationships:**
- One Member → Many Subscriptions
- One Plan → Many Subscriptions
- One Member → Many Attendance Records

---

## 📚 API Documentation

### Access Interactive Docs

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Quick API Examples

#### Create a Member
```http
POST /members/
Content-Type: application/json

{
  "name": "John Doe",
  "phone": "9876543210",
  "status": "active"
}
```

#### Create a Plan
```http
POST /plans/
Content-Type: application/json

{
  "name": "Monthly Membership",
  "price": 999,
  "duration_days": 30
}
```

#### Create a Subscription
```http
POST /subscriptions/
Content-Type: application/json

{
  "member_id": 1,
  "plan_id": 1,
  "start_date": "2025-11-27"
}
```
> **Automatic Calculation:** `end_date` is automatically calculated based on plan duration.

#### Record Attendance
```http
POST /attendance/check-in
Content-Type: application/json

{
  "member_id": 1
}
```
> **Trigger Effect:** `total_check_ins` automatically increments for the member.

#### Get All Members
```http
GET /members/?status=active
```

#### Verify Trigger Updates
```sql
SELECT id, name, total_check_ins FROM members;
```

---

## 🧪 Testing

Run the test suite using pytest:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_main.py

# Run with coverage report
pytest --cov=app tests/
```

### Example Test

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_member():
    response = client.post("/members/", json={
        "name": "Test User",
        "phone": "9999999999",
        "status": "active"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"

def test_create_plan():
    response = client.post("/plans/", json={
        "name": "Test Plan",
        "price": 1500,
        "duration_days": 30
    })
    assert response.status_code == 200
    assert response.json()["price"] == 1500
```

---

## 📊 Project Checklist

| Requirement | Status |
|-------------|--------|
| RESTful API endpoints | ✅ Complete |
| Proper data modeling | ✅ Complete |
| PostgreSQL triggers | ✅ Implemented |
| Clean code structure | ✅ Modular |
| Error handling | ✅ Included |
| Input validation | ✅ Pydantic schemas |
| API documentation | ✅ Swagger/ReDoc |
| Unit tests | ✅ Basic coverage |
| Search/Filter functionality | ✅ Implemented |
| Environment configuration | ✅ .env support |

---

## 🚀 Deployment

### Docker Support (Coming Soon)

```dockerfile
# Dockerfile example
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deployment Platforms

- **Render** - Easy deployment with PostgreSQL addon
- **Railway** - Automatic deployments from GitHub
- **AWS EC2** - Full control with scalability
- **Heroku** - Quick deployment with PostgreSQL
- **DigitalOcean** - App Platform with database

---

## 🔮 Future Enhancements

- 🔐 **JWT Authentication** - Secure API endpoints
- 🐳 **Docker Compose** - Containerized deployment
- 📧 **Email Notifications** - Membership expiry alerts
- 💳 **Payment Integration** - Stripe/PayPal support
- 📊 **Analytics Dashboard** - Member statistics and trends
- 📱 **Mobile App Integration** - REST API for mobile clients
- 🔔 **Push Notifications** - Real-time updates
- 📄 **Report Generation** - PDF receipts and invoices
- 🌐 **Multi-tenant Support** - Support for multiple gyms/centers

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- 📧 Email: your.email@example.com
- 🐙 GitHub: [@yourusername](https://github.com/yourusername)
- 💼 LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- FastAPI documentation and community
- SQLAlchemy contributors
- PostgreSQL trigger examples
- All open-source contributors

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ using FastAPI and PostgreSQL

</div>