# Holiday House Rental System

A web application for managing holiday house rentals, built with Python Flask and MySQL.


![Holiday House Rental System Homepage](https://github.com/yun88zhou/jennyzhou-Happy-Holiday-House-Rental-System/blob/main/static/bground/holidayhomepage.jpg)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technical Stack](#technical-stack)
- [Application Structure](#application-structure)
- [User Roles and Functionalities](#user-roles-and-functionalities)
- [Installation and Local Setup](#installation-and-local-setup)
- [Usage Guide](#usage-guide)
- [Test Users](#test-users)
- [Future Enhancements](#future-enhancements)
- [Resources](#resources)

## Introduction

This Flask-based web application provides a simplified Holiday House Rental System. It features a login system with role-based access control, allowing customers, staff, and administrators to interact with the system according to their permissions. While booking and rental functionalities are not implemented, the system demonstrates different levels of access and operations for various user roles.

## Features

- Secure user authentication and authorization
- Role-based dashboards (Customer, Staff, Admin)
- House listing management
- User profile management
- Responsive design using Bootstrap

## Technical Stack

- Backend: Python Flask
- Database: MySQL
- ORM: SQLAlchemy
- Frontend: HTML, CSS, Bootstrap
- Authentication: Flask-Login
- Password Hashing: bcrypt

## Application Structure
📁app
├── app.py
├── connect.py
├── holidayhouse.sql
├── 📁static/
│   ├── 📁bground/
│   ├── 📁css/
│   └── 📁houseImage/
└── 📁templates/
    ├── 📁common/
    ├── 📁customer/
    ├── 📁staff/
    ├── 📁admin/
    ├── base_customer.html
    ├── base_staff.html
    └── base_admin.html



## User Roles and Functionalities

The application supports three user roles:
1. **Customer**: Browse houses, view details, manage profile
2. **Staff**: Manage house listings, view customer information
3. **Admin**: Full system access, user management, reporting

## Installation and Local Setup

1. Clone the repository

```git clone https://github.com/yun88zhou/jennyzhou-Happy-Holiday-House-Rental-System```

2. Install required packages:
```pip install Flask Flask-MySQLdb bcrypt```

3. Configure database connection in `connect.py`:
```python

HOST = "your_database_host"
USER = "your_database_user"
PASSWORD = "your_database_password"
DB = "your_database_name"```

4.Run the application
```python app.py```

5.Access the application at http://localhost:5000


## Usage Guide

For detailed instructions on how to use the system, please refer to our User Guide.

## Test Users
| Role    |    Email                 | Notes      |
| -------  | ----------------------  | ---------- |
| Customer |  `alice@email.com`      | `13579` |
| Staff   |   `jennifer@email.com`   | `13579` |
| Admin   |   `arlette@email.com`    | `13579` |

## Future Enhancements

Implement booking and rental functionalities
Add payment integration
Enhance search and filtering options for houses
Implement a review and rating system

## Resources

House images sourced from Airbnb
Flask Documentation
MySQL Documentation



