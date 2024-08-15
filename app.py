from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import bcrypt
from connect import HOST, USER, PASSWORD, DB

app = Flask(__name__)

app.secret_key = 'justkey'

app.config['MYSQL_HOST'] = HOST
app.config['MYSQL_USER'] = USER
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = DB

mysql = MySQL(app)


@app.route('/')
@app.route('/home')
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM house')
    house = cursor.fetchall() #get house info for display on home page
    return render_template("common/home.html", houses = house)

@app.route('/home_house_details/<int:house_id>') # url get house_id by user clicking one of the pictures which bring with a house_id.
def home_house_details(house_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM house')
    houses = cursor.fetchall() # get username to display 
    houses = next((h for h in houses if h['house_id'] == house_id), None)  #get house info from database for user to view.
    if houses:
        return render_template('common/house_details.html', houses=houses)
    else:
        return redirect(url_for('home'))


############################## CUSTOMER interface starts From here ############################   
############################## CUSTOMER interface starts From here ############################   
############################## CUSTOMER interface starts From here ############################   
# Function to hash a password during registration
# def hash_password(password):
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     return hashed_password

# Function to check a password during login
def check_password(input_password, stored_hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form: #user need to enter thsee info
        session.clear()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user and check_password(password, user['password']): #check password if match
            session['loggedin'] = True
            session['user_id'] = user['user_id'] #get it just in case need it for later
            session['username'] = user['username'] 
            session['email'] = user['email']
            if user['user_type'] == 'admin': #by verify the user_type, different users access different interface.
                return redirect(url_for('admin_dashboard', username=session['username']))
            elif user['user_type'] == 'customer':
                return redirect(url_for('customer_dashboard', username=session['username']))
            elif user['user_type'] == 'staff':
                return redirect(url_for('staff_dashboard', username=session['username']))
        else:
            message = 'Please enter correct email/password!'      
    return render_template('common/login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])  
def register():
    message = ''
    if request.method == 'POST': 
        Fname = request.form['Fname'].strip()
        Lname = request.form['Lname'].strip()
        email = request.form['email'].strip()
        confirm_email = request.form['confirm_email'].strip()
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()
        user_type = "customer"
        phone_num = request.form['phone'].strip()
        address = request.form['address'].strip()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        try:
            # Check if the email already exists
            cursor.execute('SELECT * FROM user WHERE LOWER(email) = LOWER(%s)', (email,))
            account = cursor.fetchall()

            if account:
                message = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                message = 'Invalid email address!'
            elif not username or not password or not email:
                message = 'Please fill out the form!'
            else:
                if email != confirm_email:
                    message = 'Emails do not match. Please try again.'
                elif password != confirm_password:
                    message = 'Passwords do not match. Please try again.'
                else:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute('INSERT INTO user (username, password, email, user_type) VALUES (%s, %s, %s, %s)',
                                   (username, hashed_password, email, user_type))
                    mysql.connection.commit()
                    new_user_id = cursor.lastrowid

                    cursor.execute('INSERT INTO customer (user_id, c_fName, c_Lname, address, email, phone_num) VALUES (%s, %s, %s, %s, %s, %s)',
                                   (new_user_id, Fname, Lname, address, email, phone_num))
                    mysql.connection.commit()
                    
                    flash('You have successfully registered!', 'success')
                    return redirect(url_for("login"))
        except Exception as e:
            # Handle exceptions (e.g., database errors)
            print(f"Error: {e}")
            message = 'An error occurred. Please try again later.'
        finally:
            cursor.close()
    else:
        message = None
    return render_template('common/register.html', message=message)




@app.route("/customer_dashboard",methods=['GET']) # entered customer's home page
def customer_dashboard():
    if 'loggedin' in session:
        userid = session['user_id'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) # get user table info from database for display
        cursor.execute('SELECT * FROM user WHERE user_id = % s', (userid, ))
        user = cursor.fetchone()   
    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM house')
        houses = cursor.fetchall()  #get house_image to display
        return render_template("customer/customer_dashboard.html", user = user, houses=houses)
    return render_template("customer/customer_dashboard.html", userid=userid)

@app.route("/customer_account") #customer can manage their profile by clicking account button to this url
def customer_account():
    if 'loggedin' in session:
        userid = session['user_id'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) # get user table info from database for display
        cursor.execute('SELECT * FROM user WHERE user_id = % s', (userid, ))
        user = cursor.fetchone()   
        return render_template("customer/customer_account.html",user=user)
    
@app.route("/customerProfile", methods =['GET', 'POST']) #click personal info box and user will enter this url
def customerProfile():
    if 'loggedin' in session:
        viewUserId = session['user_id'] 
        if request.method == 'GET': 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE user_id = % s', (viewUserId, ))
            user= cursor.fetchone() #get username from user table to display, which will be edit later.

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer WHERE user_id = % s', (viewUserId, ))
            customer= cursor.fetchone() # get customer table info to display, which will be edit later.
            return render_template("customer/customer_profile.html",user=user,customer=customer)
        else:  #get all the values from form and get ready to update these values
            userName = request.form['username']   
            Fname = request.form['Fname']   
            Lname = request.form['Lname']   
            email = request.form['email']  
            phone = request.form['phone']
            address = request.form['address']
            new_user_id = viewUserId
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE user SET  username =% s WHERE user_id =% s', (userName, (new_user_id, ), ))#update user table to database
            mysql.connection.commit()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer WHERE user_id = % s', (new_user_id, ))
            existing_customer= cursor.fetchone() # Check if the customer have rows where  user_id =%s 
            if existing_customer:  
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#update user table to database
                cursor.execute('UPDATE customer SET  c_fName =% s,c_Lname=% s,address=% s, email=% s,phone_num=% s WHERE user_id =% s', (Fname,Lname,address,email,phone, (new_user_id, ), ))
                mysql.connection.commit() # if there is already a user_id after registration, then just update customer data.
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)# if admin has deleted customer from system, then need to insert new data in customer table.
                cursor.execute('INSERT INTO customer (user_id, c_fName,c_Lname, address, email, phone_num) VALUES (%s,%s,%s,%s,%s,%s)', (new_user_id,Fname,Lname,address,email,phone,))
                mysql.connection.commit()  
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM customer WHERE user_id = % s', (new_user_id, ))
            customer= cursor.fetchone() 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE user_id = % s', (new_user_id, ))
            user= cursor.fetchone() #get username from user table to display after update/insert data
            return render_template("customer/customer_profile.html",new_user_id=new_user_id,user=user,customer=customer)
    return redirect(url_for('login'))

@app.route('/house_details/<int:house_id>') # url get house_id by user clicking one of the pictures which bring with a house_id.
def house_details(house_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM house')
    houses = cursor.fetchall() # get username to display 
    houses = next((h for h in houses if h['house_id'] == house_id), None)  #get house info from database for user to view.
    if houses:
        return render_template('customer/customer_houseDetails.html', houses=houses)
    else:
        return redirect(url_for('customer_dashboard'))

@app.route("/password_change", methods =['GET', 'POST'])  #!!!!!!For CUSTOMER can change their password by entering new password
def password_change():
    message = ''
    if 'loggedin' in session:
        changePassUserId = session['user_id'] #get user_id from url:/customer_account and then replace 

        if request.method == 'POST' and 'old_password' in request.form and 'new_password' in request.form and 'confirm_pass' in request.form:
            old_password = request.form['old_password']
            print(old_password)
            new_password = request.form['new_password']   
            confirm_pass = request.form['confirm_pass'] 
            userId = changePassUserId
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user where user_id =%s;',(userId,))
            user = cursor.fetchone()
            print("user is",user)
            if user and check_password(old_password,user['password']):
                if new_password == confirm_pass:
                    Newpassword=bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE user SET  password =% s WHERE user_id =% s', (Newpassword, userId))
                    mysql.connection.commit()
                    message = 'Password updated !' 
                    return render_template("customer/customer_changePass.html", message = message, changePassUserId = changePassUserId) 
                else:
                    message= 'New password and confirm password do not match.'
            else:
                message= 'Invalid old password.'
        return render_template("customer/customer_changePass.html", message = message)
    return redirect(url_for('login'))
############################## CUSTOMER interface ENDS here ############################   
############################## CUSTOMER interface ENDS From here ############################   
############################## CUSTOMER interface ENDS From here ############################   





############################## ADMIN interface ENDS From here############################   
############################## ADMIN interface ENDS From here############################   
############################## ADMIN interface ENDS From here############################   
@app.route("/admin_dashboard") # user logins admin's home page
def admin_dashboard():
    if 'loggedin' in session:
        username = request.args.get('username')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user')
        users = cursor.fetchall()    

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM house')
        houses = cursor.fetchall()    
        return render_template("admin/admin_dashboard.html", users = users,username = username,houses=houses)
    return render_template("admin/admin_dashboard.html", username=username)

@app.route('/admin_houseDetails/<int:house_id>') # url get house_id by user clicking one of the pictures which bring with a house_id.
def admin_houseDetails(house_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM house')
    houses = cursor.fetchall() # get username to display 
    houses = next((h for h in houses if h['house_id'] == house_id), None)  #get house info from database for user to view.
    if houses:
        return render_template('admin/admin_houseDetails.html', houses=houses)
    else:
        return redirect(url_for('admin_dashboard'))

@app.route("/adminProfile", methods =['GET', 'POST']) #customer can manage their profile by clicking account button to this url
def adminProfile():
    if 'loggedin' in session:
        userid = session['user_id'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) # get user table info from database for display
        cursor.execute('SELECT * FROM user WHERE user_id = % s', (userid, ))
        user = cursor.fetchone()   

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE user_id = % s', (userid, ))
        admin= cursor.fetchone() # get admin table info to display, which will be edit later.
        return render_template("admin/admin_profile.html",user=user,admin=admin)

@app.route("/admin_editProfile", methods =['GET', 'POST']) #click personal info box and user will enter this url
def admin_editProfile():
    if 'loggedin' in session:
        editUserId = session['user_id'] 
        if request.method == 'GET': 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE user_id = % s', (editUserId, ))
            user= cursor.fetchone() #get username from user table to display, which will be edit later.
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute('SELECT * FROM admin WHERE user_id = % s', (editUserId, ))
            admin= cursor.fetchone() # get admin table info to display, which will be edit later.
            return render_template("admin/admin_editProfile.html",user=user,admin=admin)
        else:  #get all the values from form and get ready to update these values
            userName = request.form['username']   
            Fname = request.form['Fname']   
            Lname = request.form['Lname']   
            email = request.form['email']  
            phone = request.form['phone']
            date_joined = request.form['date_joined']
 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE user SET  username =% s WHERE user_id =% s', (userName, editUserId,))#update user table to database
            mysql.connection.commit()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#update user table to database
            cursor.execute("UPDATE admin SET  a_Lname =% s,a_Lname=% s, email=% s,phone_number=% s,date_joined=% s WHERE user_id =% s", (Fname,Lname,email,phone,date_joined,editUserId,))
            mysql.connection.commit()
            return redirect(url_for('adminProfile'))   
    return redirect(url_for('login'))


@app.route("/admin_password", methods =['GET', 'POST'])  #admin can change their password by entering new password
def admin_password():
    message = ''
    if 'loggedin' in session:
        changePassUserId = session['user_id'] #get user_id  and then replace this user_id 's password
        if request.method == 'POST' and 'old_password' in request.form and 'new_password' in request.form and 'confirm_pass' in request.form:
            old_password = request.form['old_password']
            new_password = request.form['new_password']   
            confirm_pass = request.form['confirm_pass'] 
            userId = changePassUserId
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user where user_id =%s;',(userId,))
            user = cursor.fetchone()      
            if user and check_password(old_password,user['password']):
                if new_password == confirm_pass:
                    Newpassword=bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE user SET  password =% s WHERE user_id =% s', (Newpassword, userId))
                    mysql.connection.commit()
                    message = 'Password updated !' 
                    return render_template("admin/admin_passChange.html", message = message, changePassUserId = changePassUserId) 
                else:
                    message= 'New password and confirm password do not match.'
            else:
                message= 'Invalid old password.'
        return render_template("admin/admin_passChange.html", message = message)
    return redirect(url_for('login'))
############# Above is admin manage their own profile####################



####### Below is for admin manage Customer(search,add,edit,delete)###########
@app.route("/admin_listCustomer", methods=["GET", "POST"])  #submenu on the side bar
def admin_listCustomer():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customer;")
    customer=cursor.fetchall()
    customer_list = [tuple(d.values()) for d in customer] # customer is tuple of dictionaries, so need to convert it to list 
    return render_template("admin/customer_view.html", customer_list=customer_list)
      
@app.route("/admin_searchCustomer", methods=["[GET]","POST"])   # admin can search customer details from search bar.
def admin_searchCustomer():
    if 'reset' in request.form:  # when the reset button is pressed
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM customer;")
        customer=cursor.fetchall()
        customer_list = [tuple(d.values()) for d in customer]
        return render_template("admin/customer_view.html", customer_list=customer_list)
    elif 'customername' in request.form:  # when customername is entered in search bar
        customername=request.form.get('customername').strip() #  Get the search query for customer the form data.
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM customer\
                            WHERE c_fName  Like  %s or c_Lname Like  %s\
                        order by c_fName, c_Lname;", (f'%{customername}%',f'%{customername}%',))
        customer  = cursor.fetchall()
        if customer is not None:
            customer_list = [tuple(d.values()) for d in customer]
            return render_template("admin/customer_view.html", customer_list = customer_list,customername=customername)
        else:
            customer_list = []
            return render_template("admin/customer_view.html", customer_list = customer_list,customername=customername)

@app.route("/admin_addCustomer", methods=["GET", "POST"])  # get into this route by clicking add button 
def admin_addCustomer():
    message= ''
    if request.method == "POST":
        customer_Fname = request.form["c_fName"].strip()
        customer_Lname = request.form["c_Lname"].strip()
        customer_address=request.form["address"].strip()
        customer_email=request.form["email"].strip()
        customer_ph_num=request.form["phone"].strip()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE LOWER(email) = LOWER(%s)', (customer_email,))
        account = cursor.fetchone() #get the matched user's info for use
        if account: # check if user already in database 
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', customer_email): # verify if user enter a valid email address format
            message = 'Invalid email address!'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO customer\
                                (c_fName, c_Lname, address, email, phone_num)\
                                VALUES (%s, %s, %s, %s, %s);", (customer_Fname, customer_Lname, customer_address, customer_email, customer_ph_num,))
            mysql.connection.commit()  #Commit the changes to the database
            message = 'You have successfully add a customer!'
            return redirect(url_for('admin_listCustomer'))
    return render_template("admin/customer_add.html",message=message)


@app.route("/admin_editCustomer", methods=["GET", "POST"])   # this route will get one of the edit button to update this customer(which include a user_id)
def admin_editCustomer():
    if request.method == 'GET': 
        customer_id=request.args.get('customer_id')
         #get all the values from form and get ready to update these values
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE customer_id = % s', (customer_id, ))
        customer= cursor.fetchone() # get admin table info to display, which will be edit later.
        return render_template("admin/customer_update.html",customer=customer)
    else:    
        customer_id=request.form["customer_id"]
        customer_Fname = request.form["c_fName"].strip()
        customer_Lname = request.form["c_Lname"].strip()
        customer_address=request.form["address"].strip()
        customer_email=request.form["email"].strip()
        customer_ph_num=request.form["phone"].strip()
 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#update customer table to database
        cursor.execute("UPDATE customer SET  c_fName =% s,c_Lname=% s, address=% s,email=% s,phone_num=% s WHERE customer_id =% s;", (customer_Fname,customer_Lname,customer_address,customer_email, customer_ph_num,(customer_id, ), ))
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM customer;")
        customer=cursor.fetchall()
        customer = [tuple(d.values()) for d in customer]
        return redirect(url_for('admin_listCustomer'))
 

@app.route("/admin_deleteCustomer", methods=["GET", "POST"])   # this route will get one of the delete button to update this customer(which include a user_id)
def admin_deleteCustomer():
    if request.method == 'GET': 
        customer_id=request.args.get('customer_id')
         #get all the values from form and get ready to update these values
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE customer_id = % s', (customer_id, ))
        customer= cursor.fetchone() # get admin table info to display, which will be deleted later.
    
        return render_template("admin/customer_delete.html",customer=customer)
    else:    
        customer_id=request.form["customer_id"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#delete customer table to database
        cursor.execute("DELETE FROM customer WHERE customer_id = %s;", (customer_id,))
        mysql.connection.commit()
        return redirect(url_for('admin_listCustomer'))
####### Above is for admin manage Customer(search,add,edit,delete)##########################
 


####### Below is for admin manage staff(search,add,edit,delete)##########################
@app.route("/admin_listStaff", methods=["GET", "POST"])  #submenu on the side bar
def admin_listStaff():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM staff;")
    staff=cursor.fetchall()
    staff_list = [tuple(d.values()) for d in staff] # staff is tuple of dictionaries, so need to convert it to list 
    return render_template("admin/staff_view.html", staff_list=staff_list)
      
@app.route("/admin_searchStaff", methods=["[GET]","POST"])   # admin can search staff details from search bar.
def admin_searchStaff():
    if 'reset' in request.form:  # when the reset button is pressed
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM staff;")
        staff=cursor.fetchall()
        staff_list = [tuple(d.values()) for d in staff]
        return render_template("admin/staff_view.html", staff_list=staff_list)
    elif 'staffname' in request.form:  # when staffname is entered in search bar
        staffname=request.form.get('staffname').strip() #  Get the search query for staff the form data.
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM staff\
                            WHERE s_fName  Like  %s or s_Lname Like  %s\
                        ;", (f'%{staffname}%',f'%{staffname}%',))
        staff  = cursor.fetchall()
        if staff is not None:
            staff_list = [tuple(d.values()) for d in staff]
            return render_template("admin/staff_view.html", staff_list = staff_list,staffname=staffname)
        else:
            staff_list = []
            return render_template("admin/staff_view.html", staff_list = staff_list,staffname=staffname)

@app.route("/admin_addStaff", methods=["GET", "POST"])  # get into this route by clicking add button 
def admin_addStaff():
    message= ''
    if request.method == "POST":
        staff_Fname = request.form["s_fName"].strip()
        staff_Lname = request.form["s_Lname"].strip()
        staff_date=request.form["date_joined"].strip()
        staff_email=request.form["email"].strip()
        staff_ph_num=request.form["phone"].strip()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staff WHERE LOWER(email) = LOWER(%s)', (staff_email,))
        account = cursor.fetchone() #get the matched user's info for use
        if account: # check if user already in database 
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', staff_email): # verify if user enter a valid email address format
            message = 'Invalid email address!'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO staff\
                                (s_fName, s_Lname, email, phone_number, date_joined)\
                                VALUES (%s, %s, %s, %s, %s);", (staff_Fname, staff_Lname, staff_email, staff_ph_num, staff_date,))
            mysql.connection.commit()  #Commit the changes to the database
            return redirect(url_for('admin_listStaff'))
    return render_template('admin/staff_add.html', message=message)


@app.route("/admin_editStaff", methods=["GET", "POST"])   # this route will get one of the edit button to update this staff(which include a staff_id)
def admin_editStaff():
    if request.method == 'GET': 
        staff_id=request.args.get('staff_id') #get all the values from form and get ready to update these values
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staff WHERE staff_id = % s', (staff_id, ))
        staff= cursor.fetchone() # get admin table info to display, which will be edit later.
        return render_template("admin/staff_update.html",staff=staff)
    else:    
        staff_id=request.form["staff_id"]
        staff_Fname = request.form["s_fName"].strip()
        staff_Lname = request.form["s_Lname"].strip()
        staff_date=request.form["date_joined"] 
        staff_email=request.form["email"].strip()
        staff_ph_num=request.form["phone"].strip()
 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#update staff table to database
        cursor.execute("UPDATE staff SET  s_fName =% s,s_Lname=% s, email=% s,phone_number=% s,date_joined=% s WHERE staff_id =% s;", (staff_Fname,staff_Lname,staff_email,staff_ph_num, staff_date,(staff_id, ), ))
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM staff;")
        staff=cursor.fetchall()
        staff = [tuple(d.values()) for d in staff]
        return redirect(url_for('admin_listStaff'))
 

@app.route("/admin_deleteStaff", methods=["GET", "POST"])   # this route will get one of the delete button to update this staff(which include a user_id)
def admin_deleteStaff():
    if request.method == 'GET': 
        staff_id=request.args.get('staff_id')
         #get all the values from form and get ready to update these values
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staff WHERE staff_id = % s', (staff_id, ))
        staff= cursor.fetchone() # get admin table info to display, which will be deleted later.
    
        return render_template("admin/staff_delete.html",staff=staff)
    else:    
        staff_id=request.form["staff_id"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#delete staff table to database
        cursor.execute("DELETE FROM staff WHERE staff_id = %s;", (staff_id,))
        mysql.connection.commit()
        return redirect(url_for('admin_listStaff'))
 ####### Above is for admin manage staff list(search,add,edit,delete)###############################



####### Below is for admin house(search,add,edit,delete)##########################
@app.route("/admin_listHouse", methods=["GET", "POST"])  #submenu on the side bar
def admin_listHouse():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM house;")
    house=cursor.fetchall()
    house_list = [tuple(d.values()) for d in house] # house is tuple of dictionaries, so need to convert it to list 
    return render_template("admin/house_view.html", house_list=house_list)
      
@app.route("/admin_searchHouse", methods=["[GET]","POST"])   # admin can search house details from search bar.
def admin_searchHouse():
    if 'reset' in request.form:  # when the reset button is pressed
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM house;")
        house=cursor.fetchall()
        house_list = [tuple(d.values()) for d in house]
        return render_template("admin/house_view.html", house_list=house_list)
    elif 'house_content' in request.form:  # when house_id is entered in search bar
        house_content=request.form.get('house_content').strip() #  Get the search query for house the form data.
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM house\
                            WHERE house_id=% s OR h_address Like  %s or house_title LIKE %s\
                        ;", (house_content,f'%{house_content}%',f'%{house_content}%',)) 
        house  = cursor.fetchall() 
        if house is not None: 
            house_list = [tuple(d.values()) for d in house]
            return render_template("admin/house_view.html", house_list = house_list,house_content=house_content)
        else:
            house_list = [] 
            return render_template("admin/house_view.html", house_list = house_list,house_content=house_content)
        
@app.route("/admin_addHouse", methods=["GET", "POST"])  # get into this route by clicking add button 
def admin_addHouse():
    message= ''
    if request.method == "POST":
        h_address = request.form["h_address"].strip()
        bedroom_num = request.form["bedroom_num"]
        bathroom_num=request.form["bathroom_num"] 
        max_occupancy=request.form["max_occupancy"] 
        rental_per_night=request.form["rental_per_night"].strip()
        house_image=request.form["house_image"].strip()
        house_title=request.form["house_title"].strip()
        house_description=request.form["house_description"].strip()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM house WHERE LOWER(h_address) = LOWER(%s)', (h_address,))
        account = cursor.fetchone() #get the matched user's info for use
        if account: # check if user already in database 
            message = 'House already exists!'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO house\
                                (h_address, bedroom_num, bathroom_num, max_occupancy, rental_per_night,house_image,house_title,house_description)\
                                VALUES (%s, %s,%s,%s, %s, %s, %s,%s);", (h_address, bedroom_num, bathroom_num, max_occupancy, rental_per_night,house_image,house_title,house_description,))
            mysql.connection.commit()  #Commit the changes to the database
            return redirect(url_for('admin_listHouse'))
    return render_template('admin/house_add.html', message=message)


@app.route("/admin_editHouse", methods=["GET", "POST"])   # this route will get one of the edit button to update this house(which include a house_id)
def admin_editHouse():
    if request.method == 'GET': 
        house_id=request.args.get('house_id') #get all the values from form and get ready to update these values
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM house WHERE house_id = % s', (house_id, ))
        house= cursor.fetchone() # get admin table info to display, which will be edit later.
        return render_template("admin/house_update.html",house=house)
    else:    
        house_id=request.form["house_id"]
        h_address = request.form["h_address"].strip()
        bedroom_num = request.form["bedroom_num"]
        bathroom_num=request.form["bathroom_num"] 
        max_occupancy=request.form["max_occupancy"] 
        rental_per_night=request.form["rental_per_night"].strip()
        house_image=request.form["house_image"].strip()
        house_title=request.form["house_title"].strip()
        house_description=request.form["house_description"].strip()
 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#update house table to database
        cursor.execute("UPDATE house SET  h_address =% s,bedroom_num=% s, bathroom_num=% s,max_occupancy=% s,\
                       rental_per_night=% s,house_image=% s,house_title =% s,house_description =% s WHERE house_id =% s;", \
                        (h_address,bedroom_num,bathroom_num,max_occupancy,rental_per_night,house_image,house_title,house_description, (house_id, ), ))
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM house;")
        house=cursor.fetchall()
        house = [tuple(d.values()) for d in house]
        return redirect(url_for('admin_listHouse'))
 

@app.route("/admin_deleteHouse", methods=["GET", "POST"])   # this route will get one of the delete button to update this house(which include a user_id)
def admin_deleteHouse():
    if request.method == 'GET': 
        house_id=request.args.get('house_id')
         #get all the values from form and get ready to update these values
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM house WHERE house_id = % s', (house_id, ))
        house= cursor.fetchone() # get admin table info to display, which will be deleted later.
        return render_template("admin/house_delete.html",house=house)
    else:    
        house_id=request.form["house_id"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#delete house table to database
        cursor.execute("DELETE FROM house WHERE house_id = %s;", (house_id,))
        mysql.connection.commit()
        return redirect(url_for('admin_listHouse'))
 ####### Above is for admin manage house list(search,add,edit,delete)##########################################################
############################## ADMIN interface ENDS here ##################V###############   
############################## ADMIN interface ENDS  here ##################################   
############################## ADMIN interface ENDS  here ##################################   
 


####--------------------------------------STAFF interface starts here--------------------------------------------------------------------------------
###----------------------------------------STAFF interface starts here----------------------------------------------------------------------------------
###-----------------------------------------STAFF interface starts here----------------------------------------------------------------------
@app.route("/staff_dashboard") 
def staff_dashboard():
    if 'loggedin' in session:
        username = request.args.get('username')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user')
        users = cursor.fetchall()    

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM house')
        houses = cursor.fetchall()    
        return render_template("staff/staff_dashboard.html", users = users,username = username,houses=houses)
    return render_template("staff/staff_dashboard.html", username=username)

@app.route('/staff_houseDetails/<int:house_id>') # url get house_id by user clicking one of the pictures which bring with a house_id.
def staff_houseDetails(house_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM house')
    houses = cursor.fetchall() # get username to display 
    houses = next((h for h in houses if h['house_id'] == house_id), None)  #get house info from database for user to view.
    if houses:
        return render_template('staff/staff_houseDetails.html', houses=houses)
    else:
        return redirect(url_for('staff_dashboard'))



@app.route("/staffProfile", methods =['GET', 'POST']) #click personal info box and user will enter this url
def staffProfile():
    if 'loggedin' in session:
        viewUserId = session['user_id'] 
        if request.method == 'GET': 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE user_id = % s', (viewUserId, ))
            user= cursor.fetchone() #get user_id from user table to display, which will be edit later.

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM staff WHERE user_id = % s', (viewUserId, ))
            staff= cursor.fetchone() # get staff table info to display, which will be edit later.
            return render_template("staff/staff_profile.html",user=user,staff=staff)
        else:  #get all the values from form and get ready to update these values
            userName = request.form['username']   
            Fname = request.form['Fname']   
            Lname = request.form['Lname']   
            email = request.form['email']  
            phone = request.form['phone'] 
            date_joined = request.form['date_joined']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE user SET  username =% s WHERE user_id =% s', (userName, (viewUserId, ), ))#update user table to database
            mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#update user table to database
            cursor.execute("UPDATE staff SET  s_fName =% s,s_Lname=% s, email=% s,phone_number=% s,date_joined=% s WHERE user_id =% s", (Fname,Lname,email,phone,date_joined,viewUserId,))
            mysql.connection.commit()
            return redirect(url_for('staffProfile')) 
    return redirect(url_for('login'))

@app.route("/staff_editProfile", methods =['GET', 'POST']) #click personal info box and user will enter this url
def staff_editProfile():
    if 'loggedin' in session:
        editUserId = session['user_id'] 
        if request.method == 'GET': 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE user_id = % s', (editUserId, ))
            user= cursor.fetchone() #get username from user table to display, which will be edit later.
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM staff WHERE user_id = % s', (editUserId, ))
            staff= cursor.fetchone() # get staff table info to display, which will be edit later.
            return render_template("staff/staff_editProfile.html",user=user,staff=staff)
        else:  #get all the values from form and get ready to update these values
            userName = request.form['username']   
            Fname = request.form['Fname']   
            Lname = request.form['Lname']   
            email = request.form['email']  
            phone = request.form['phone']
            date_joined = request.form['date_joined']
            message="Profile updated!"
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE user SET  username =% s WHERE user_id =% s', (userName, editUserId,))#update user table to database
            mysql.connection.commit()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#update user table to database
            cursor.execute("UPDATE staff SET  s_fName =% s,s_Lname=% s, email=% s,phone_number=% s,date_joined=% s WHERE user_id =% s", (Fname,Lname,email,phone,date_joined,editUserId,))
            mysql.connection.commit()
            return redirect(url_for('staffProfile'))   
    return redirect(url_for('login'))



@app.route("/staff_password", methods =['GET', 'POST'])  #staff can change their password by entering new password
def staff_password():
    message = ''
    if 'loggedin' in session:
        changePassUserId = session['user_id'] #get user_id from session and then replace the password for this user_id
        print("changeUserid is",changePassUserId)
        if request.method == 'POST' and 'old_password' in request.form and 'new_password' in request.form and 'confirm_pass' in request.form:
            old_password = request.form['old_password']
            new_password = request.form['new_password']   
            confirm_pass = request.form['confirm_pass'] 
            userId = changePassUserId
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user where user_id =%s;',(userId,))
            user = cursor.fetchone()      
            if user and check_password(old_password,user['password']):
                if new_password == confirm_pass:
                    Newpassword=bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('UPDATE user SET  password =% s WHERE user_id =% s', (Newpassword, userId))
                    mysql.connection.commit()
                    message = 'Password updated !' 
                    return render_template("staff/staff_passChange.html", message = message, changePassUserId = changePassUserId) 
                else:
                    message= 'New password and confirm password do not match.'
            else:
                message= 'Invalid old password.'
        return render_template("staff/staff_passChange.html", message = message)
    return redirect(url_for('login'))
############# Above staff manage their own profile####################



####### Below is for staff manage Customer(search,add,edit,delete)###########
@app.route("/staff_listCustomer", methods=["GET", "POST"])  
def staff_listCustomer():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM customer;")
    customer=cursor.fetchall()
    customer_list = [tuple(d.values()) for d in customer] # customer is tuple of dictionaries, so need to convert it to list 
    return render_template("staff/staff_customer_view.html", customer_list=customer_list)
      
@app.route("/staff_searchCustomer", methods=["[GET]","POST"])   # staff can search customer details from search bar.
def staff_searchCustomer():
    if 'reset' in request.form:  # when the reset button is pressed
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM customer;")
        customer=cursor.fetchall()
        customer_list = [tuple(d.values()) for d in customer]
        return render_template("staff/staff_customer_view.html", customer_list=customer_list)
    elif 'customername' in request.form:  # when customername is entered in search bar
        customername=request.form.get('customername').strip() #  Get the search query for customer the form data.
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM customer\
                            WHERE c_fName  Like  %s or c_Lname Like  %s\
                        order by c_fName, c_Lname;", (f'%{customername}%',f'%{customername}%',))
        customer  = cursor.fetchall()
        if customer is not None:
            customer_list = [tuple(d.values()) for d in customer]
            return render_template("staff/staff_customer_view.html", customer_list = customer_list,customername=customername)
        else:
            customer_list = []
            return render_template("staff/staff_customer_view.html", customer_list = customer_list,customername=customername)

####-------------------------------------------------------------------------------------------------------------------------------------------
###--------------------------------------Staff manage house list-----------------------------------------------------------------------------------------
@app.route("/staff_listHouse", methods=["GET", "POST"])  
def staff_listHouse():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM house;")
    house=cursor.fetchall()
    house_list = [tuple(d.values()) for d in house] # house is tuple of dictionaries, so need to convert it to list 
    return render_template("staff/staff_house_view.html", house_list=house_list)
      
@app.route("/staff_searchHouse", methods=["[GET]","POST"])   # staff can search house details from search bar.
def staff_searchHouse():
    if 'reset' in request.form:  # when the reset button is pressed
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM house;")
        house=cursor.fetchall()
        house_list = [tuple(d.values()) for d in house]
        return render_template("staff/staff_house_view.html", house_list=house_list)
    elif 'house_content' in request.form:  # when house_id is entered in search bar
        house_content=request.form.get('house_content').strip() #  Get the search query for house the form data.
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM house\
                            WHERE house_id=% s OR h_address Like  %s or house_title LIKE %s\
                        ;", (house_content,f'%{house_content}%',f'%{house_content}%',)) 
        house  = cursor.fetchall() 
        if house is not None: 
            house_list = [tuple(d.values()) for d in house]
            return render_template("staff/staff_house_view.html", house_list = house_list,house_content=house_content)
        else:
            house_list = [] 
            return render_template("staff/staff_house_view.html", house_list = house_list,house_content=house_content)
        
@app.route("/staff_addHouse", methods=["GET", "POST"])  # get into this route by clicking add button 
def staff_addHouse():
    message= ''
    if request.method == "POST":
        h_address = request.form["h_address"].strip()
        bedroom_num = request.form["bedroom_num"]
        bathroom_num=request.form["bathroom_num"] 
        max_occupancy=request.form["max_occupancy"] 
        rental_per_night=request.form["rental_per_night"].strip()
        house_image=request.form["house_image"].strip()
        house_title=request.form["house_title"].strip()
        house_description=request.form["house_description"].strip()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM house WHERE LOWER(h_address) = LOWER(%s)', (h_address,)) #address should be unique
        account = cursor.fetchone() #get the matched user's info for use
        if account: # check if user already in database 
            message = 'House already exists!'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO house\
                                (h_address, bedroom_num, bathroom_num, max_occupancy, rental_per_night,house_image,house_title,house_description)\
                                VALUES (%s, %s,%s,%s, %s, %s, %s,%s);", (h_address, bedroom_num, bathroom_num, max_occupancy, rental_per_night,house_image,house_title,house_description,))
            mysql.connection.commit()  #Commit the changes to the database
            return redirect(url_for('staff_listHouse'))
    return render_template('staff/staff_house_add.html', message=message)


@app.route("/staff_editHouse", methods=["GET", "POST"])   # this route will get one of the edit button to update this house(which include a house_id)
def staff_editHouse():

    if request.method == 'GET': 
        house_id=request.args.get('house_id') #get all the values from form and get ready to update these values
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM house WHERE house_id = % s', (house_id, ))
        house= cursor.fetchone() # get staff table info to display, which will be edit later.
        return render_template("staff/staff_house_update.html",house=house)
    else:    
        house_id=request.form["house_id"]
        h_address = request.form["h_address"].strip()
        bedroom_num = request.form["bedroom_num"]
        bathroom_num=request.form["bathroom_num"] 
        max_occupancy=request.form["max_occupancy"] 
        rental_per_night=request.form["rental_per_night"].strip()
        house_image=request.form["house_image"].strip()
        house_title=request.form["house_title"].strip()
        house_description=request.form["house_description"].strip()
 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#update house table to database
        cursor.execute("UPDATE house SET  h_address =% s,bedroom_num=% s, bathroom_num=% s,max_occupancy=% s,\
                       rental_per_night=% s,house_image=% s,house_title =% s,house_description =% s WHERE house_id =% s;", \
                        (h_address,bedroom_num,bathroom_num,max_occupancy,rental_per_night,house_image,house_title,house_description, (house_id, ), ))
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM house;")
        house=cursor.fetchall()
        house = [tuple(d.values()) for d in house]
        return redirect(url_for('staff_listHouse'))
 

@app.route("/staff_deleteHouse", methods=["GET", "POST"])   # this route will get one of the delete button to update this house(which include a user_id)
def staff_deleteHouse():
    if request.method == 'GET': 
        house_id=request.args.get('house_id')
         #get all the values from form and get ready to update these values
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM house WHERE house_id = % s', (house_id, ))
        house= cursor.fetchone() # get staff table info to display, which will be deleted later.
        return render_template("staff/staff_house_delete.html",house=house)
    else:    
        house_id=request.form["house_id"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)#delete house table to database
        cursor.execute("DELETE FROM house WHERE house_id = %s;", (house_id,))
        mysql.connection.commit()
        return redirect(url_for('staff_listHouse'))

###-------------------------------------------------STAFF interface ends here---------------------------------------------------------------------------
###------------------------------------------------STAFF interface ends here-----------------------------------------------------------------------
###------------------------------------------------STAFF interface ends here-------------------------------------------------------------------------


@app.route('/logout') #clear the infomation in session when logout
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('username', None)
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)