# Mediqe 

**Comprehensive Backend Platform for Healthcare & Medical Solutions**

---
 
## 📖 Project Overview

Mediqe is a modular, scalable backend system designed for healthcare applications, featuring robust user management, appointment scheduling, medical records, doctor-patient consultations, and admin/role-based dashboards. Built with modern Python/Django best practices and ready for production deployment.

--- 

## 🏗 Applications Structure

**All the following are Django apps located in the `appointment_mediqe/` directory:**

- **accounts** Handles user authentication, registration, permissions, and role management (doctor, patient, admin).
- **appointment_mediqe** Main Django project configuration app (settings, URLs, WSGI/ASGI, etc.).
- **appointments** Manages creation, scheduling, and tracking of doctor-patient appointments.
- **chats** Implements chat functionality for real-time or asynchronous communication between patients and doctors.
- **dashboards** Provides dashboards and summary views for various user roles (admin, doctor, patient).
- **healthdatas** Handles the storage and retrieval of general health data for users (e.g., vitals, health history).
- **medical_records** Manages secure storage of patient medical records, prescriptions, and related files.
- **notifications** Sends notifications and system alerts to users (via email, push, or in-app).
- **organizations** Manages healthcare organizations, clinics, and their relationships with users.
- **payments** Handles payment processing, transaction history, and integration with payment gateways.

All of these are Django applications and should be added to `INSTALLED_APPS` in your Django settings.

---

## ⚙️ Technologies Used

**Backend:**
- Django 4.x
- Django REST Framework (DRF)
- PostgreSQL
- Redis (asynchronous tasks)
- Celery (background jobs, notifications)
- JWT Authentication (SimpleJWT)
- Docker & Docker Compose

**Frontend (planned):**
- React + Axios
- Tailwind CSS or Material UI

**DevOps & Tools:**
- Git + GitHub (team collaboration)
- Swagger / ReDoc for interactive API docs
- pytest + coverage for testing (TDD)
- CI/CD with GitHub Actions (optional)

---

## 🗓️ 6-Week Timeline

**Week 1: Project Initialization**
- Set up repository, virtual environments, Docker, and base Django project/apps
- Static/media configuration, base templates

**Week 2: User Authentication**
- Custom user model, registration, login, and role-based access
- JWT authentication setup

**Week 3: Appointments Module**
- Models for doctor availability and patient appointment booking
- REST APIs for viewing and booking appointments

**Week 4: Medical Records Module**
- Models: MedicalRecord, Prescription, UploadedFile
- Secure file uploads and access control

**Week 5: Consultations System**
- Real-time/asynchronous chat logic (messages, file attachments)
- APIs for sending/receiving patient-doctor messages

**Week 6: Dashboard & Finishing Touches**
- Role-based dashboards for admin, doctors, patients
- Final testing, docs, and deployment preparation
#.
---

## 👥 Team Structure

- **Pouria (Team Lead)**: Oversees all modules, project setup, architecture, authentication, background tasks, and documentation
- **Zeinab**: Focuses on medical records and consultation modules
- **AmirHossein**: Responsible for appointments module, dashboard, and overall testing

---

## 📝 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/pooriya-cloudS/mediqe.git
   cd mediqe
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env` and update with your settings

4. **Run locally**
   ```bash
   docker-compose up --build
   # or with Django
   python manage.py runserver
   ```

5. **API Docs**
   - Visit `/docs` (Swagger/ReDoc) after running the server

---

## 🧪 Testing

To run tests:
```bash
pytest
```
or
```bash
python manage.py test
```

---

## 🤝 Contributions

Contributions, issues, and feature requests are welcome!  
See [issues](https://github.com/pooriya-cloudS/mediqe/issues).

---

## 📄 License

This project is licensed under the MIT License.

---
