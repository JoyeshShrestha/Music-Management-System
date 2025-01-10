from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DB_USERNAME:DB_PASSWORD@DB_HOST/DB_NAME'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


@app.route('/',methods=['GET','POST'])
def register():
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


