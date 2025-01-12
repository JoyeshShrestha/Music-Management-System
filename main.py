from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

import pymysql
import os
from dotenv import load_dotenv
from user import User


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DB_USERNAME:DB_PASSWORD@DB_HOST/DB_NAME'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy()
# db.init_app(app)

# Database connection configuration
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
# DB_NAME = os.getenv('DB_NAME')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to fetch user by ID
        query = "SELECT * FROM user WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_tuple = cursor.fetchone()

        cursor.close()
        connection.close()

        # Return a User object if a user is found
        if user_tuple:
            return User.from_tuple(user_tuple)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Establish a database connection
def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database="music_management",
          port=3305
    )
    return connection
def create_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Raw SQL to create a table
        create_table_query =  """
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(500) NOT NULL,
            phone VARCHAR(20),
            dob DATETIME,
            gender ENUM('m', 'f', 'o') DEFAULT 'o',
            address VARCHAR(255),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'User' created successfully!")
        cursor.close()
        connection.close()
    except Exception as e:
        print( f"An error occurred: {e}")
 
      




def check_email_exists(email):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Use a parameterized query to prevent SQL injection
        check_email_query = "SELECT * FROM user WHERE email = %s"
        cursor.execute(check_email_query, (email,))

        # Fetch the first matching user
        user_tuple = cursor.fetchone()

        cursor.close()
        connection.close()

        # Return True if user exists, otherwise False
        if user_tuple:
            return User.from_tuple(user_tuple)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def insert_data_user(first_name, last_name, date_of_birth, gender, email, password, phone, address):
    try:
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Use parameterized queries to prevent SQL injection
        insert_table_query = """
        INSERT INTO user (first_name, last_name, email, password, phone, dob, gender, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        # Execute the query with parameters
        cursor.execute(insert_table_query, (first_name, last_name, email, password, phone, date_of_birth, gender, address))

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Flash success message and redirect to login
        flash("User inserted successfully!")
        return redirect(url_for("login"))

    except Exception as e:
        # Handle exceptions and flash error message
        flash(f"An error occurred: {e}")
        return redirect(url_for("register"))
                 






@app.route('/',methods=['GET','POST'])
def register():
    # create_table()
    print(DB_PASSWORD)
    if request.method == "POST":
         
        # try:
            email=request.form.get('email')

            user = check_email_exists(email)

            if user:
                flash("You've already signed up with that email, log in instead!")

                return redirect(url_for("login"))

            
            
            first_name = request.form["FirstName"]
            last_name = request.form["LastName"]
            date_of_birth = request.form["date_of_birth"]
            gender = request.form["gender"]
            phone = request.form["Phone"]
            if not phone.isdigit() or len(phone) != 10:
                flash(f"An error occurred: {e}")
                return redirect(url_for("register"))
            address = request.form["Address"]
            password = generate_password_hash(request.form["password"],method='pbkdf2:sha256',salt_length=8)

            insert_data_user(first_name,last_name,date_of_birth,gender,email,password,phone,address)

        #  try:
        #      email = request.form.get('email')
        #      result = db.session.execute(db.select(User).where(User.email == email))
        #      user = result.scalar()
        #      if user:
        #          flash("You've already signed up with that email, log in instead!")
        #          return redirect(url_for('login'))
        #      register = User(
        #      name = user_name,
        #      email = email,
        #      password = generate_password_hash(request.form["password"],method='pbkdf2:sha256',salt_length=8)
        #         )
        #      db.session.add(register)
        #      db.session.commit()
        #  except:
        #      return redirect(url_for("login"))

        #     login_user(register)
        #  return redirect(url_for("secrets",name=user_name))

            
    # return render_template("register.html",logged_in=current_user.is_authenticated)
    return render_template("register.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
       
     
        user = check_email_exists(email)
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))

        # Verify the password
        if not check_password_hash(user.password, password):
            flash("Incorrect Password!")
            return redirect(url_for('login'))

        # Log in the user
        login_user(user)
        flash("Logged in successfully!")
        return redirect(url_for('dashboard'))  

    return render_template("login.html")

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user_email = current_user.email, logged_in=True)    

if __name__=="__main__":
    app.run(debug=True)


