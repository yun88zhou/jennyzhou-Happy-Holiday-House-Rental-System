# A Simple Holiday House Rental System with Python Flask and MySQL
<br>

<a href="https://liyunzhou1156273.pythonanywhere.com/" target="_blank">https://liyunzhou1156273.pythonanywhere.com/
</a>
<br>

<img src="https://github.com/liyunzhou1156273/1156273_assignment1_639/blob/main/static/bground/holidayhomepage.jpg">

<br>

## Table of Contents
* [Introduction](#intro)
* [App Structure and Implementation](#structure)
* [User, Customer, Staff and Admin Guide](#guide)
* [Running Locally](#local)
* [Test Users](#test)
* [Resources](#resources)
  
<a id='intro'></a>
## Introduction
<p align="justify">
This is a Flask Python Web App for a Holiday House Rental System.The application includes a 
login system and separate dashboards for three user roles: customer, staff and admin.Some of these include HTML, CSS, Flask, SQLAlchemy, Bootstrap, Virtual Environments, and so on. Users should able to login to the system and access their respective dashboards as well as to perform specific actions related to holiday house rental operations. This is a simplified version without the booking and rental functionalities as the focus is on providing different level of access for different user roles.
</p>
<br>


<a id='structure'></a>
## App Structure and Implementation
<p align="justify">
This project is implemented in Python and organized as a simple package, as outlined below:
</p>


📁app<br>
&emsp;app.py <br>
&emsp;connect.py <br>
&emsp;holidayhouse.sql<br>
&emsp;📁static/ <br>
&emsp;&emsp; 📁bground/ <br>
&emsp;&emsp; 📁css/ <br>
&emsp;&emsp; 📁houseImage/ <br>
&emsp;📁templates/ <br>
&emsp; &emsp; 📁common/ <br>
&emsp; &emsp; 📁customer/ <br>
&emsp; &emsp; 📁staff/ <br>
&emsp; &emsp; 📁admin/ <br>
&emsp; &emsp; base_customer/ <br>
&emsp; &emsp; base_staff/ <br>
&emsp; &emsp; base_admin/ <be>

- An overview of the routes for admin, customer, and staff functionalities within a single flowchart.

<img src="https://github.com/liyunzhou1156273/1156273_assignment1_639/blob/main/static/bground/structure.png">
<p align="justify"> 
While working on this project locally, MySQL database and Workbench were utilized. Workbench was specifically used for creating the database and viewing tables. The core functionality is encapsulated in the app.py file, which contains login details (email and password) for customers, staff, and admin. Additionally, it includes a script using MySQLdb.cursors to update, add, and delete details to the database.
</p>
<be>

<a id='guide'></a>
## User, Customer, Staff and Admin Guide
You can find the website's usage guide [here](https://github.com/Oyebamiji-Micheal/Result-Management-System-with-Python-Flask-and-MySQL/blob/master/guide.md).
<br><be>

<a id='local'></a>
## Running Locally 
<p align="justify">
Python 3.11.1 was used at the time of building this project. For Windows users, make sure Python is added to your PATH. <br>
<strong>1. Install Required Packages</strong><br>
- Install Flask and Flask-MySQLdb. Additionally, you'll need bcrypt for password hashing. Here are the commands to install these packages:<br>
  
```
pip install Flask Flask-MySQLdb bcrypt
```

<strong>2.Connect database</strong><br>
```
# connect.py
HOST = "your_database_host"
USER = "your_database_user"
PASSWORD = "your_database_password"
DB = "your_database_name"
```
- Replace "your_database_host", "your_database_user", "your_database_password", and "your_database_name" with your actual MySQL database details in connect.py file.


<strong>3.Run the Flask Application</strong><br>
- In your terminal or command prompt, navigate to the directory containing your app.py file and run the following command:
```
python app.py
```
<strong>4.Access the Web Application</strong><br>
- Open your web browser and navigate to http://127.0.0.1:5000/ or http://localhost:5000/'.


<a id='test'></a>
## Test Users

| Role    |    Email                 | Notes      |
| -------  | ----------------------  | ---------- |
| Customer |  `alice@email.com`      | `13579` |
| Staff   |   `jennifer@email.com`   | `13579` |
| Admin   |   `arlette@email.com`    | `13579` |




<a id='resources'></a>
## Resources
 
All house images are from here:<a href="https://www.airbnb.co.nz/" target="_blank">Airbnb</a> 
