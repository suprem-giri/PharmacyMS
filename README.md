# 💊 Pharmacy Management System

A web-based **Pharmacy Management System (PMS)** built with **Python and Django** to manage medicines, customers, orders, doctor appointments, prescriptions, suppliers, and pharmacy operations.

The project was developed as a BCA project with a focus on applying backend development, database design, authentication, and real-world business workflows.

---

## 📌 Overview

Managing pharmacy operations manually can make it difficult to keep track of medicines, orders, prescriptions, appointments, and suppliers.

This project provides a centralized web application where different users can perform pharmacy-related tasks through role-based dashboards and workflows.

The system focuses on:

* Medicine Management
* Customer management
* Medicine ordering
* Order status tracking
* Doctor appointments
* Prescription management
* Supplier management
* Supplier restocking requests
* Dashboard statistics
* Medicine stock and expiry monitoring

---

## ✨ Key Features

### 👤 Authentication & User Roles

* User registration and login
* Django authentication
* Role-based access
* Customer, Doctor/Staff workflows
* Admin-controlled access where applicable

### 💊 Medicine Management

* Add and manage medicines
* Store medicine information and pricing
* Track available quantity
* Monitor low-stock medicines
* Monitor medicines approaching expiry
* View medicine details

### 🛒 Order Management

* Customers can place medicine orders
* Order and order-item management
* Cart-based ordering workflow
* Order total calculation
* Track order status
* Support for different order states such as:

  * Pending
  * Completed
  * Cancelled

### 👨‍⚕️ Doctor Appointments

* Doctor information management
* Doctor specialization
* Customer appointment requests
* Appointment date and reason
* Appointment management

### 📋 Prescription Management

* Prescription records
* Prescription items
* Doctor/customer relationship
* Prescription workflow

### 🏪 Supplier Management

* Supplier records
* Supplier contact information
* Restocking requests
* Supplier request tracking

### 📊 Dashboard

The application provides dashboard information such as:

* Total medicines
* Low-stock medicines
* Expiring medicines
* Pending orders
* Pending appointments
* Supplier requests
* Prescription information
* Sales-related statistics

---

## 🏗️ Technology Stack

| Category             | Technology              |
| -------------------- | ----------------------- |
| Programming Language | Python                  |
| Backend Framework    | Django                  |
| Database             | SQLite                  |
| Frontend             | HTML5, CSS3, JavaScript |
| UI                   | Bootstrap               |
| Authentication       | Django Authentication   |
| ORM                  | Django ORM              |
| Version Control      | Git & GitHub            |

---

## 🗄️ Main Data Models

The system uses relational database models to represent the application's core business entities.

Some of the main entities include:

```text
User
 │
 ├── Customer
 │
 └── Doctor

Medicine

Order
 └── OrderItem

Doctor
 └── Appointment

Prescription
 └── PrescriptionItem

Supplier
 └── SupplierRequest
```

The relationships between these entities allow the system to manage customers, medicines, orders, doctors, prescriptions, and suppliers within a single application.

---

## 🔐 Security & Access Control

The application uses Django's built-in authentication system and separates functionality based on user roles.

Important backend considerations include:

* Authentication before accessing protected functionality
* Role-based access to dashboards
* Server-side form validation
* Protection of user-specific records
* Environment-specific configuration
* Secret values kept outside source control

---

## 📊 Business Rules

Some of the application's business logic includes:

* Medicines with quantity at or below the configured threshold are identified as low stock.
* Medicines approaching their expiry date can be highlighted.
* Orders maintain a defined status.
* Orders contain one or more order items.
* Appointments connect customers with doctors.
* Prescriptions contain prescription items.
* Suppliers can receive restocking requests.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have installed:

* Python 3.x
* pip
* Git

### 1. Clone the repository

```bash
git clone YOUR_PMS_REPOSITORY_URL
cd YOUR_PMS_REPOSITORY_NAME
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If the repository does not currently contain `requirements.txt`, generate it from your working environment:

```bash
pip freeze > requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

### 6. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 📸 Screenshots

Add screenshots of the actual application here.

Recommended screenshots:

### Login / Registration

```text
screenshots/login.png
```

### Dashboard

```text
screenshots/dashboard.png
```

### Medicine Management

```text
screenshots/medicine-management.png
```

### Orders

```text
screenshots/orders.png
```

### Appointments

```text
screenshots/appointments.png
```

### Prescriptions

```text
screenshots/prescriptions.png
```

> Screenshots should show the real application rather than mockups.

---

## 📁 Suggested Project Structure

```text
pharmacy-management-system/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── app/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
├── static/
├── media/
└── screenshots/
```

> Update this section to match your actual project structure before publishing.

---

## 🧪 Testing

Testing is an area of the project that I am continuing to improve.

Important areas for automated testing include:

* User authentication
* Role-based permissions
* Medicine validation
* Order creation
* Order status changes
* Stock updates
* Appointment creation
* Prescription handling
* Supplier requests

Example command:

```bash
python manage.py test
```

---

## 🔮 Future Improvements

Planned improvements include:

* Django REST Framework API
* PostgreSQL support
* Automated test coverage
* Improved role-based permissions
* API documentation
* Better error handling
* Production deployment
* Docker support
* Improved database query optimization
* Email notifications
* More detailed reporting

---

## 🎓 Academic Project

This project was developed as part of my **Bachelor of Computer Applications (BCA)** learning journey.

It helped me gain practical experience with:

* Python
* Django
* Relational databases
* Django ORM
* Authentication
* Business logic
* Web application architecture
* Git and GitHub

---

## 👨‍💻 Author

**Suprem Giri**

BCA Student | Aspiring Python/Django Backend Developer

GitHub:
https://github.com/suprem-giri

---

⭐ If you find this project useful or interesting, consider giving the repository a star.
