from flaskblog.models import User
from flask import render_template, url_for, redirect, flash,request
#importing db  for connecting routes to the datbase and instance variable bcrypt which is created in the __init__.py for decrypting password
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user,logout_user




posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html', title='Home',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/profile")
def profile():
    return render_template('profile.html',title='User Profile')



@app.route("/login", methods=['GET', 'POST'])
def login():
    #redirecting the current user to the home page if user is already logged in using current_user() function of flask_login lib.
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = LoginForm()
    if form.validate_on_submit():

        #checking for email  if the given email id is already in the database or not.
        user = User.query.filter_by(email=form.email.data).first()
        #checking for the password entered by the user matches with the password in the database.
        if user and bcrypt.check_password_hash(user.password,form.password.data):

            #Making user login  using login_user() function of flask_login lib.
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')

            #flashing successfull message when user logged in.and  #redirecting to next page after login
            flash('You have been logged in!', 'success')
            return next_page if next_page else redirect (url_for('home'))
        else:
            #flashing unsuccessfull message if email or pass is not matched, and redirecting to the login page
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    #inbuilt function called as logout_user() from the flask_login package.
    logout_user()
    return redirect(url_for('home'))



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
         # generating a hash code for the password entered by the  new user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # geting  the information about the new user from the html form(Registrationform)
        user = User(username=form.username.data,email=form.email.data, password=hashed_password)

        #adding  this user to the database
        db.session.add(user)

        #making this change permanent
        db.session.commit()

        # after adding user displaying a successfull message
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
        #sending  registered user  to  login page
    return render_template('register.html', title='Register', form=form)


