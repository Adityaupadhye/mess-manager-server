
# **Mess Management System API**

### *Efficiently manage hostel mess attendance and food preferences using RFID/QR technology and data analytics*

## Overview

The **Mess Management System** is a Django REST API-based project designed to streamline and manage hostel mess activities. By using RFID/QR code to capture student attendance during meals (breakfast, lunch, dinner, etc.), the system records data, which is further analyzed to provide insights and trends, such as weekly meal patterns, the number of attendees per meal, and food preferences.

This project integrates **data analytics** and **visualization** to ensure seamless management of the hostel mess while providing valuable insights into food consumption patterns. 

---

## Setup

Clone this repository
`git clone https://github.com/Adityaupadhye/mess-manager-server.git`

Setup python virtual environment
```
mkdir -p ~/.virtualenvs/
python -m venv  ~/.virtualenvs/mess-app-dev
source ~/.virtualenvs/mess-app-dev/bin/activate
pip install -r requirements.txt
```

Setup a mysql database (local or hosted)

Set up environment variables
```
cp .env.example .env
```

Update values in `.env` according to your database connection details


---

## **Key Features**

- **Student RFID/QR Integration**: Records student attendance for meals in real-time using RFID technology.
- **Meal Tracking**: Track attendance for different meal categories such as breakfast, lunch, and dinner.
- **Data Analytics**: Perform trend analysis on collected data to reveal insights such as:
  - Daily, weekly, and monthly meal attendance patterns.
  - Number of students attending each meal.
  - Most popular meals and student food preferences.
- **Visualization**: Generate charts and graphs to visually represent data trends and send them to the frontend.
- **Secure Login**: Secure login for users with role-based access control (students, mess admins, etc.).
  
---

## **Technologies Used**

- **Backend**:
  - Django
  - Django REST Framework
  - Python

- **Database**:
  - SQLite

- **Data Visualization**:
  - Matplotlib
  - Seaborn
  - Plotly

- **Frontend**:
  - HTML, CSS
  - AngularJS
  - Chart.js

---


## **Data Visualization and Analytics**

This project utilizes Python libraries such as **Matplotlib** and **Plotly** to analyze and visualize mess entry data:

- **Meal Attendance**: The system analyzes student attendance at meals and displays visual trends, such as which meals (breakfast, lunch, or dinner) have the highest attendance.
- **Weekly/Monthly Trends**: The system identifies patterns in student attendance over time, enabling mess administrators to make informed decisions on resource management.

These visualizations are generated as PNG images and sent to the frontend for user interaction.

---

## **How It Works**

1. **User Registration & Login**:
   - Users (students and admins) can log in securely to the system via the provided API. Their roles are stored in the user model, allowing for customized access to the data.

2. **RFID/QR Data Entry**:
   - When a student scans their RFID card/QR code, their attendance is recorded in the `Foodlog` model. This entry includes the roll number, meal category, timestamp, and role (student/admin).

3. **Data Analysis**:
   - Using collected data, admins can request analysis results, which are returned in the form of graphs or charts. These analyses help in optimizing food resources and understanding food consumption patterns.

---

### Team: 
    - Mohammad Kashif Khan (24M0770)
    - Mohammad Aasim (24M2118)
    - Aditya Upadhye (24M0830)

## **Contact**

For any queries or feedback, feel free to reach out:

- **Name**: Mohammad Kashif Khan
- **Email**: [](kashifkhan@cse.iitb.ac.in)
- **GitHub**: [Silent-Learner](https://github.com/silent-learner)
