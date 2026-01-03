# Dayflow – Human Resource Management System  [ Made By Dhyati Jungi ]

> Every workday, perfectly aligned.

## Overview

Dayflow is a streamlined, local-first Human Resource Management System (HRMS) designed to simplify essential workforce operations. Built for simplicity and efficiency, Dayflow enables organizations to manage employees, track attendance, handle leave requests, and view payroll details without the complexity of enterprise-scale software.

This project was built by **Team Innovax** as a Minimum Viable Product (MVP) for the hackathon, demonstrating a functional, secure, and user-friendly solution for modern HR needs.

## Features

*   **Role-Based Authentication**: Secure login with distinct access levels for HR Managers (Admin) and Employees.
*   **Employee Management**: HR can add, edit, and view employee profiles, including department, role, and salary details.
*   **Attendance Tracking**:
    *   One-click Check-in and Check-out.
    *   Real-time status updates (Present, Absent, Half-day).
    *   Historical attendance logs.
*   **Leave Management**:
    *   Employees can apply for Paid, Sick, or Unpaid leave.
    *   HR can review, approve, or reject requests.
    *   Smart validation prevents overlapping leave dates.
*   **Payroll System**:
    *   Automated calculation of Net Wage (Base + Bonus - Deductions).
    *   HR can adjust bonuses and deductions.
    *   Employees have read-only access to their payslips.
*   **Interactive Dashboard**: Real-time metrics for Total Employees, Attendance, and Pending Requests, along with a "Recent Activity" feed.
*   **Realistic Demo Data**: The system auto-populates with a robust set of demo users and records for instant testing.

## Tech Stack

*   **Backend**: Python, Flask (Microframework)
*   **Frontend**: HTML5, CSS3, Responsive Design
*   **Database**: SQLite (Relational, Serverless)
*   **Security**: Session-based authentication, Role-Based Access Control (RBAC)

## Project Folder Structure

```text
flask_mvp/
├── app.py                # Main application logic and routing
├── dayflow.db            # SQLite database (auto-generated)
├── requirements.txt      # Python dependencies
├── static/               # Static assets
│   ├── css/              # Stylesheets
│   └── images/           # Images and logos
└── templates/            # HTML Templates (Jinja2)
    ├── base.html         # Layout master file
    ├── login.html        # Authentication page
    ├── dashboard.html    # Main dashboard
    ├── employees.html    # Employee list (HR)
    ├── attendance.html   # Attendance tracker
    ├── leaves.html       # Leave management
    └── payroll.html      # Salary details
```

## Installation & Setup (Mac/Linux)

Follow these steps to run Dayflow locally:

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd Dayflow-HRMS/flask_mvp
    ```

2.  **Create Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Application**
    ```bash
    python3 app.py
    ```

5.  **Access the App**
    Open your browser and navigate to: `http://localhost:8000`

## Demo Credentials

Use the following credentials to test different user roles:

| Role | Email | Password |
| :--- | :--- | :--- |
| **HR Manager** | `admin@dayflow.com` | `admin` |
| **Employee** | `john@dayflow.com` | `user` |
| **Employee** | `jane@dayflow.com` | `user` |

## Usage Guide

### HR Workflow
1.  **Login** as Admin.
2.  **Dashboard**: View daily stats and recent activities.
3.  **Employees**: Add new staff members using the "Add Member" button.
4.  **Leaves**: Go to the Leave section to Approve/Reject pending requests.
5.  **Payroll**: Update bonuses or tax deductions for any employee.

### Employee Workflow
1.  **Login** as Employee.
2.  **Attendance**: Click "Check In" at the start of the day and "Check Out" when leaving.
3.  **Leaves**: Submit a new leave request via the "Apply Leave" button.
4.  **Payroll**: View your current month's salary breakdown.

## Screenshots

### Dashboard
*(Add screenshot here)*

### Employee Management
*(Add screenshot here)*

### Attendance Log
*(Add screenshot here)*

## Known Limitations

*   **Database**: Uses SQLite, intended for local development and testing only (not for concurrent production use).
*   **Deployment**: configured for local execution; production implementation would require WSGI server (Gunicorn/uWSGI).
*   **Payroll**: Basic implementation for demo purposes; does not include complex tax slabs or statutory compliance.

## Future Enhancements

*   **Email Notifications**: Automated alerts for leave status changes.
*   **Report Export**: CSV/PDF export for attendance and payroll data.
*   **Enhanced Payroll**: Comprehensive tax calculation engine.
*   **REST API**: Fully separated frontend (React/Vue) and backend API.
*   **Mobile App**: Native mobile interface for on-the-go access.

## Team & Credits

* Team Innovax *
*   This project was developed as a submission for the Hackathon.
*   Designed and built by Team Innovax.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
