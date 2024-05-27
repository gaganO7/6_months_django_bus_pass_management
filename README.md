# Bus Pass Management System

## Overview

The Bus Pass Management System is designed to streamline the process of applying for and managing college bus passes. This web-based application allows students to apply for bus passes based on their respective routes and desired duration (3 months or 6 months). The system also includes administrative functions to manage routes, pass prices, bus details, and handle student applications and issues. This project is built using the Django framework and SQLite database.

## Features

### Admin Module

- **CRUD Operations for Bus Routes:** Admin can create, read, update, and delete bus routes.
- **CRUD Operations for Pass Prices:** Admin can set and modify prices for 3-month and 6-month passes.
- **CRUD Operations for Bus Details:** Admin can manage details of buses operating on different routes.
- **Manage Student Applications:** Admin can review, approve, or reject bus pass applications submitted by students.
- **Handle Student Issues:** Admin can respond to issues reported by students and update the status of these issues.
- **Generate and Update Pass Status:** Admin can generate bus passes and update their status as needed.

### Student Module

- **User Registration and Login:** Students can create an account and log in to access the system.
- **View Available Passes:** Students can check the availability of bus passes based on their selected route and duration.
- **Apply for Passes:** Students can apply for bus passes according to their requirements.
- **Check Application Status:** Students can monitor the status of their bus pass applications.
- **Report Issues:** Students can report issues related to bus passes and check the status of these reported issues.
- **Purchase Passes:** Students can select a pass based on their route and buy it.

## Technology Stack

- **Backend Framework:** Django (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript (optional for dynamic functionality)

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Django

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/gagaO7/bus-pass-management.git
   cd bus-pass-management
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
