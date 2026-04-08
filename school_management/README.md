# School Management System

A comprehensive, full-featured School Management System built with Django, featuring modern UI, role-based access control, and complete CRUD operations.

## Features

### User Roles
- **Admin**: Full system control with analytics dashboard
- **Teacher**: Class management, attendance, and marks
- **Student**: Profile, attendance, marks, and fee status

### Core Modules
- Student Management (CRUD, profiles, enrollment)
- Teacher Management (assignments, profiles)
- Class & Subject Management
- Attendance System (marking, tracking, reports)
- Results & Marks Management
- Fee Management (collections, status tracking)

### Technical Features
- REST API with Django REST Framework
- AJAX for dynamic updates
- Chart.js for analytics visualization
- PDF/CSV export capabilities
- Mobile responsive design
- Role-based access control
- CSRF protection

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd school_management
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Load sample data (optional):
```bash
python manage.py shell < scripts/load_sample_data.py
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Visit `http://127.0.0.1:8000`

### Default Credentials
After creating superuser:
- Username: admin
- Password: (your chosen password)

## Project Structure

```
school_management/
├── core/              # Base templates and authentication
├── users/             # User management and profiles
├── students/          # Student-specific features
├── teachers/          # Teacher-specific features
├── academics/         # Classes and subjects
├── attendance/        # Attendance management
├── results/           # Marks and results
├── fees/              # Fee management
├── static/            # CSS, JS, images
└── media/             # Uploaded files
```

## API Endpoints

API is available at `/api/`

- `GET/POST /api/students/` - List/create students
- `GET/PUT/DELETE /api/students/{id}/` - Student detail
- `GET/POST /api/teachers/` - List/create teachers
- `GET/POST /api/attendance/` - Attendance records
- `GET/POST /api/results/` - Results records
- `GET/POST /api/fees/` - Fee records

## Technologies Used

- **Backend**: Django 5.0
- **API**: Django REST Framework
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Charts**: Chart.js
- **Database**: SQLite (default), PostgreSQL-ready
- **PDF Generation**: ReportLab
- **Excel Export**: OpenPyXL

## License

MIT License
