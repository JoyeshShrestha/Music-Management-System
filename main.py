from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

import pymysql
import os
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DB_USERNAME:DB_PASSWORD@DB_HOST/DB_NAME'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy()
# db.init_app(app)

# Database connection configuration
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
# DB_NAME = os.getenv('DB_NAME')

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
 
      














@app.route('/',methods=['GET','POST'])
def register():
    create_table()
    print(DB_PASSWORD)
    if request.method == "POST":
            pass
            # # user_name = request.form["name"]
            # # try:
            # #     email = request.form.get('email')
            # #     result = db.session.execute(db.select(User).where(User.email == email))
            # #     user = result.scalar()
            # #     if user:
            # #         flash("You've already signed up with that email, log in instead!")
            # #         return redirect(url_for('login'))
            # #     register = User(
            # #     name = user_name,
            # #     email = email,
            # #     password = generate_password_hash(request.form["password"],method='pbkdf2:sha256',salt_length=8)
            # #     )
            # #     db.session.add(register)
            # #     db.session.commit()
            # # except:
            # #     return redirect(url_for("login"))

            # login_user(register)
            # return redirect(url_for("secrets",name=user_name))

            
    # return render_template("register.html",logged_in=current_user.is_authenticated)
    return render_template("register.html")


if __name__=="__main__":
    app.run(debug=True)


