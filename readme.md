# 🎓 BBD Student Hub - Django Dashboard

This is a Django-based Student Dashboard built for easy tracking of enrolled courses, credits, grades, and attendance.

## Features
* User Registration, Login, and Logout.
* Personalized dashboard showing enrolled courses and attendance.
* Dynamic Bar Chart using Chart.js for visualizing course credits.
* Downloadable PDF Grade Reports using ReportLab.
* Real-time table updates using HTMX.
* Admin panel to manage users, courses, and attendance.

## Tech Stack
* Backend: Django 5.0, Python
* Frontend: HTML, Bootstrap 5, Chart.js, HTMX
* Database: SQLite (default)

## Setup and Run Instructions

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows use: myenv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   
3. **Run the server:**
   ```bash
   python manage.py runserver

4. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   

5. **Start the development server:**
   ```bash
   python manage.py runserver

6. **Open http://127.0.0.1:8000/login/ in your browser.**