from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from db import get_db_connection

from user_db import User_db
from artist_db import Artist_db
from user import User
import os
from dotenv import load_dotenv


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


user_db =User_db()
artist_db = Artist_db()

load_dotenv()



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



@app.route('/',methods=['GET','POST'])
def register():
  
    if request.method == "POST":
         
        # try:
            email=request.form.get('email')

            user = user_db.check_email_exists(email)

            if user:
                flash("You've already signed up with that email, log in instead!")

                return redirect(url_for("login"))

            
            
            first_name = request.form["FirstName"]
            last_name = request.form["LastName"]
            date_of_birth = request.form["date_of_birth"]
            gender = request.form["gender"]
            phone = request.form["Phone"]
            if not phone.isdigit() or len(phone) != 10:
                flash(f"An error occurred")
                return redirect(url_for("register"))
            address = request.form["Address"]
            password = generate_password_hash(request.form["password"],method='pbkdf2:sha256',salt_length=8)

            is_insert = user_db.insert_data_user(first_name,last_name,date_of_birth,gender,email,password,phone,address)
            if is_insert:
                return render_template("login.html")
    return render_template("register.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
       
     
        user = user_db.check_email_exists(email)
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))

        # Verify the password
        if not check_password_hash(user.password, password):
            flash("Incorrect Password!")
            return redirect(url_for('login'))

        # Log in the user
        login_user(user)
        return redirect(url_for('dashboard'))  

    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    print("User logged out")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user_email = current_user.email, logged_in=True)    




@app.route('/dashboard/users/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    user_db.delete_user_query(user_id)
    return redirect(url_for('get_all_users'))



@app.route('/dashboard/users')
@login_required
def get_all_users():
   
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        per_page = 4
        users, total_users = user_db.get_data_users(page,per_page)    
        total_pages = (total_users + per_page - 1) // per_page
        print(current_user.id)
        return render_template("user.html", all_users=users,logged_in = current_user.is_authenticated,login_id = current_user.id,current_page=page,
        total_pages=total_pages)

    return render_template("login.html", all_users=users,logged_in = current_user.is_authenticated)


@app.route('/dashboard/users/adduser',methods=['GET','POST'])
@login_required
def add_user():
    
    if request.method == "POST":
         
        # try:
            email=request.form.get('email')

            user = user_db.check_email_exists(email)

            if user:
                flash("You've already signed up with that email, log in instead!")

                return redirect(url_for("add_user"))

            
            
            first_name = request.form["FirstName"]
            last_name = request.form["LastName"]
            date_of_birth = request.form["date_of_birth"]
            gender = request.form["gender"]
            phone = request.form["Phone"]
            if not phone.isdigit() or len(phone) != 10:
                flash(f"An error occurred")
                return redirect(url_for("register"))
            address = request.form["Address"]
            password = generate_password_hash(request.form["password"],method='pbkdf2:sha256',salt_length=8)

            user_db.insert_data_user(first_name,last_name,date_of_birth,gender,email,password,phone,address)

            return redirect(url_for("get_all_users"))

    return render_template("adduser.html")


@app.route('/dashboard/users/edituser/<int:user_id>',methods=['GET','POST'])
@login_required
def edit_user(user_id):
    
    user = user_db.get_user_data(user_id)

    if request.method == "POST":

        first_name = request.form["FirstName"]
        last_name = request.form["LastName"]
        date_of_birth = user['dob']
        gender = request.form["gender"]
        phone = request.form["Phone"]
        address = request.form["Address"]

        user_db.update_data_user(user_id,first_name,last_name,date_of_birth,gender,user['email'],user['password'],phone,address)

        return redirect(url_for("get_all_users"))

    print(user)
    
    print(user['email'])
    return render_template("edituser.html", user=user)



@app.route('/dashboard/artists')
@login_required
def get_all_artists():
   
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        per_page = 4
        artists, total_artists = artist_db.get_data_artists(page,per_page)    
        total_pages = (total_artists + per_page - 1) // per_page
        print(artists)
        return render_template("artist.html", all_artists=artists,logged_in = current_user.is_authenticated,login_id = current_user.id,current_page=page,total_pages=total_pages)

    return render_template("dashboard.html", logged_in = current_user.is_authenticated)

@app.route('/dashboard/artists/addartist',methods=['GET','POST'])
@login_required
def add_artist():
    
    if request.method == "POST":
         
        # try:
            name=request.form.get('Name')

            artist = artist_db.check_name_exists(name)

            if artist:
                flash("This name exists already!")

                return redirect(url_for("add_artist"))

            
            
            address = request.form["Address"]
            first_release = request.form["first_release"]
            date_of_birth = request.form["date_of_birth"]

            gender = request.form["gender"]
            number_albums = request.form["number_albums"]
            
            

            artist_db.insert_data_artist(name,number_albums,first_release,date_of_birth,gender,address)

            return redirect(url_for("get_all_artists"))

    return render_template("addartist.html")

@app.route('/dashboard/artist/delete/<int:artist_id>')
@login_required
def delete_artist(artist_id):
    artist_db.delete_artist_query(artist_id)
    return redirect(url_for('get_all_artists'))



@app.route('/dashboard/artists/editartist/<int:artist_id>',methods=['GET','POST'])
@login_required
def edit_artist(artist_id):
    
    artist = artist_db.get_artist_data(artist_id)
    print(artist)

    if request.method == "POST":
        name=artist['name']

        

            
            
        address = request.form["Address"]
        first_release = request.form["first_release"]
        date_of_birth = request.form["date_of_birth"]

        gender = request.form["gender"]
        number_albums = request.form["number_albums"]
        
        date_of_birth = artist['dob']
       

        artist_db.update_data_user(artist_id,name,number_albums,first_release,date_of_birth,gender,address)

        return redirect(url_for("get_all_artists"))

    
    return render_template("editartist.html", artist=artist)


if __name__=="__main__":
    app.run(debug=True)


