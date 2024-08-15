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
* [Student and Admin Guide](#guide)
* [Running Locally](#local)
* [Contributing](#contribute)
* [Terms and Conditions](#terms)
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
<br>
app
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
&emsp; &emsp; base_customer/ <br>
&emsp; &emsp; base_staff/ <br>
&emsp; &emsp; base_admin/ <br>
&emsp;app.py <br>
&emsp;connect.py <br>
&emsp;holidayhouse.sql<br>

<p align="justify"> 
While working on this project locally, MySQL database and Workbench were utilized. Workbench was specifically used for creating the database and viewing tables. The core functionality is encapsulated in the app.py file, which contains login details (email and password) for customers, staff, and admin. Additionally, it includes a script usingMySQLdb.cursors to update,add, and delete details to the database.
</p>
<br>

<a id='guide'></a>
## Student and Admin Guide
You can find the website's usage guide [here](https://github.com/Oyebamiji-Micheal/Result-Management-System-with-Python-Flask-and-MySQL/blob/master/guide.md).
<br><br>

<a id='local'></a>
## Running Locally 
<p align="justify">
Python 3.10.6 was used at the time of building this project. For Windows users, make sure Python is added to your PATH.  <br>
Virtual environment. It is advisable to run this project inside of a virtual environment to avoid messing with your machine's primary dependencies. To get started, navigate to this project's directory, <code>Result-Management-System-with-Python-Flask-and-MySQL</code>, on your local machine. Then...
</p>

### 1. Create an environment <br>
**Windows** (cmd) <br>
```
cd Result-Management-System-with-Python-Flask-and-MySQL
pip install virtualenv
python -m virtualenv venv
```
or
```
python3 -m venv venv
```

**macOS/Linux** <br>
```
cd Result-Management-System-with-Python-Flask-and-MySQL
pip install virtualenv
python -m virtualenv venv
```

### 2. Activate environment <br>
**Windows** (cmd)

```
venv\scripts\activate
```

**macOS/Linux**

```
. venv/bin/activate
```
or
```
source venv/bin/activate
```

### 3. Install the Requirements
Windows/macOS/Linux <br>
```pip install -r requirements.txt```

### 4. Create a Database Connection
<p align="justify">
I used Xampp server to create a base. Then used Flask-SQLAlchemy along with a MySQL database to set up connections and define tables. You can use your own local or external database. But first, you need to create the database somewhere and configure its connection to the app in <code>__init__.py</code> file. For a complete list of connection URIs head over to the SQLAlchemy documentation under <a href="https://docs.sqlalchemy.org/en/14/core/engines.html" target="_blank">Supported Database</a>. This here shows some common connection strings.

SQLAlchemy indicates the source of an Engine as a URI combined with optional keyword arguments to specify options for the Engine. The form of the URI is:

```dialect+driver://username:password@host:port/database```

Many of the parts in the string are optional. If no driver is specified the default one is selected (make sure to not include the + in that case).

PostgreSQL <br>
```postgresql://scott:tiger@localhost/project``` 

MySQL / MariaDB <br>
```mysql://scott:tiger@localhost/project```

SQLite (note that platform path conventions apply): <br>
Unix/Mac (note the four leading slashes) <br>
```sqlite:////absolute/path/to/foo.db```

Windows (note 3 leading forward slashes and backslash escapes) <br>
```sqlite:///C:\\absolute\\path\\to\\foo.db```

Windows (alternative using raw string) <br>
```r'sqlite:///C:\absolute\path\to\foo.db'```
</p>

### 5. Create Tables and Define Login Details
<p align="justify">
Once you have created and connected to your database, the next step is to login system as a role or a browser in the application .

Login details. The login details for customers, staff and admin are added automatically. To use your own custom login details, register the emails and passwords in route:"/register". 
</p>

### 6. Run app

Make sure you are in this project's root directory then run the file below <br>
```python app.py```

 
 

<a id='resources'></a>
## Resources
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)
- [Flask-Admin](https://flask-admin.readthedocs.io/en/latest/index.html)
- [SQLAlchemy](https://www.sqlalchemy.org/)
<br>

<img src="https://pbs.twimg.com/media/FdvOGhYWYAApxKW?format=jpg&name=900x900">