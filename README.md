# Attendance Management System

A desktop-based **Attendance Management System** developed using **Python (Tkinter)** and **MySQL**. The system allows faculty members to manage student attendance and enables students to view their attendance percentage subject-wise.

---

## Features

### Student Module
- View attendance by entering Register Number
- Select Department, Semester, and Division
- Display subject-wise attendance percentage
- Highlight attendance below 75%
- View faculty assigned to each subject

### Faculty Module
- Faculty login using Faculty ID
- Mark attendance for students
- Select subject and attendance date
- Toggle attendance status (Present/Absent)
- Save attendance into MySQL database
- View subject-wise attendance report
- Display attendance percentage of all students

---

## Technologies Used

- Python 3.x
- Tkinter (GUI)
- ttk Widgets
- tkcalendar
- MySQL 8.x
- mysql-connector-python

---

## Project Structure

```
Attendance_System/
│
├── attendance_system.py      # Main Python application
├── attendance_db.sql         # MySQL database
├── README.md
```

---

## Database Schema

The project uses the following tables:

- department
- semester
- division
- faculty
- student
- subject
- attendance

### Relationships

```
Department
      │
Semester
      │
Division
      │
Student ───── Attendance ───── Subject ───── Faculty
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Soya-dev-code/attendance-management-system.git
```

### 2. Install dependencies

```bash
pip install mysql-connector-python
pip install tkcalendar
```

### 3. Import Database

Open MySQL Workbench and import

```
attendance_db.sql
```

or execute

```sql
SOURCE attendance_db.sql;
```

### 4. Configure MySQL

Edit the database connection in the Python file.

```python
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="attendance_db"
)
```

Replace

```
your_password
```

with your own MySQL password.

### 5. Run the project

```bash
python attendance_system.py
```

---

## How to Use

### Student

1. Select Student Login
2. Select Department
3. Select Semester
4. Select Division
5. Enter Register Number
6. Click **Check Attendance**
7. View subject-wise attendance percentage

---

### Faculty

1. Select Faculty Login
2. Enter Faculty ID
3. Login
4. Select Subject
5. Select Date
6. Load Students
7. Double-click a student to change Present/Absent
8. Submit Attendance

---

## Attendance Calculation

Attendance percentage is calculated as

```
Attendance % =
(Number of Present Classes / Total Classes)
× 100
```

Students having attendance below **75%** are highlighted.

---

## Sample Modules

### Student Window

- Register Number Verification
- Attendance Percentage
- Faculty Details
- Subject-wise Report

### Faculty Window

- Attendance Entry
- Attendance Report
- Subject Selection
- Date Selection

---

## Requirements

- Python 3.10+
- MySQL Server 8.x
- MySQL Workbench (optional)
- Windows/Linux

Python Libraries

```
mysql-connector-python
tkcalendar
tkinter
```

---

## Future Enhancements

- Department → Semester → Division based student filtering
- Faculty password authentication
- Edit existing attendance
- Attendance graphs
- Export attendance to Excel
- PDF report generation
- Admin module
- Student login using password
- Search and filter functionality

---

## Screenshots

## Learning Outcomes

This project demonstrates:

- Python GUI Development
- Tkinter Widgets
- MySQL Database Connectivity
- SQL Queries
- CRUD Operations
- Event Handling
- Database Design
- Attendance Management Logic

---

## Author

**Soya Devassia**

B.Tech Computer Science and Engineering

---

## License

This project is developed for academic and educational purposes.
