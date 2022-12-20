# flask_login_logout
#Project Outlines and Layout
database coding for our application. 

we will be using sqlalchamy orm
 
ORM - object relational mapper. allows us to easily use our database and map them with the parameters of the columns of the database tables.

advantage of ORM and sqlalchamy is we can use this to connect to multiple databases without changing the python code.

All we need to do is pass the different url's of the databases (mysql, postgresql, sqlite3, etc ) and it will connect automatically. 

we will use sqlite3 database. 

step 1 :- install sqlalchamy package. using pip installer

pip install flask-sqlalchamy

step2 :- import this library on top of the main file . of your application.  from flask_sqlalchemy import SQLAlchemy

flaskblog.py

from flask_sqlalchemy import SQLAlchemy

now we need to mention the uri (internal link to connect to database. ) of the database to sqlalchamy to connect it. 
and we need to set this as a configuration in our app at the top. 


step 3:- we configure the database uri for the sqlite3 database and database name site.db. 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///site.db'


step 4 :- instantiate the SQLAlchemy() and pass the app our application name which we have kept using the constructor. 
db = SQLAlchemy(app)

step5 :- is to create the user models. as classes. for each users. who will use this application. 

flaskblog.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class User(db.Model):
    # columns of the tables. 
    id = db.Column(db.Integer, primary_key = True)
    username   = db.Column(db.String(20),  unique   = True,  nullable = False)
    email      = db.Column(db.String(120), unique   = True,  nullable = False)
    image_name = db.Column(db.String(20),  nullable = False, default = 'default.jpg')
    password   = db.Column(db.String(60),  nullable = False) 
    # setting a relationship between author and the posts ( one to many.- one person can write as many post as possbile , but every post will have only one author.)
    # note this will not be a new column. its just a relationship which will run in the background.
    posts = db.relationship('Post', backref = 'author', lazy = True)
    # lazy = True . sqlalchemy will load the data only when it is required . (not all at ones. )

    # a repr() function - represent function used to print how our object is going to get printed . 
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_name}')" 


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    # making the foreign key for the author who wrote the post. 
    user_if = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    # here user.id is the table name and id is the column name in the user table.

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')" 



step 6 :- now we will use these two models to create the database along with tables and columns. from command prompt in your virtual environment. 

go to the cmd., open the virtualenv , activated and type . 
python
to start coding in python. 

from flaskblog import db

# now we can create the database using the command. 
db.create_all()


 
 command line code. 


(myenv) C:\Users\user\Desktop\blog_website>python
Python 3.9.12 (main, Apr  4 2022, 05:22:27) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32

Warning:
This Python interpreter is in a conda environment, but the environment has
not been activated.  Libraries may fail to load.  To activate this environment
please see https://conda.io/activation

Type "help", "copyright", "credits" or "license" for more information.
>>> from flaskblog import db
>>> db.create_all()



some queries. 

(myenv) C:\Users\user\Desktop\blog_website>python
Python 3.9.12 (main, Apr  4 2022, 05:22:27) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32

Warning:
This Python interpreter is in a conda environment, but the environment has
not been activated.  Libraries may fail to load.  To activate this environment
please see https://conda.io/activation

Type "help", "copyright", "credits" or "license" for more information.
>>> from flaskblog import db
>>> db.create_all()
>>> from flaskblog import User, Post
>>> user_1 = User(username = "john" , email = "john@gmail.com" , password = "password")
>>> db.session.add(user_1)
>>> user_2 = User(username = "jane" , email = "jane@gmail.com" , password = "password")
>>> db.session.add(user_2)
>>> db.session.commit()
>>> User.query.all()
[User('john', 'john@gmail.com', 'default.jpg'), User('jane', 'jane@gmail.com', 'default.jpg')]
>>> User.query.first()
User('john', 'john@gmail.com', 'default.jpg')
>>> User.query.filter_by(username = 'john').all()
[User('john', 'john@gmail.com', 'default.jpg')]
>>> User.query.filter_by(username = 'john').first()
User('john', 'john@gmail.com', 'default.jpg')



# we can store this user inside a variable. and later use that variable. to accesss all the columns from the database table.  

>>> user = User.query.filter_by(username = 'john').first()
>>> user.id
1
>>> user.username
'john'
>>> user.email
'john@gmail.com'
>>> user.password
'password'
>>> user = User.query.get(1)
>>> user
User('john', 'john@gmail.com', 'default.jpg')
>>> user.posts
[]                      # empty posts for this user right now. 


# lets add some posts. by the user with id as 1. 
>>> post_1 = Post(title = "Blog 1", content = "First Blog post." ,  user_id = user.id)
# no need to provide the date. it will populate itself. cos we have used the utcnow.


>>> post_1 = Post(title = "Blog 1", content = "First Post Content", user_if = user.id)
>>> post_2 = Post(title = "Blog 2", content = "Second Post Content", user_if = user.id)
>>> db.session.add(post_1)
>>> db.session.add(post_2)
>>> db.session.commit()

# to see all the posts by user_if  =  1. 

>>> user.posts
[Post('Blog 1', '2022-12-13 07:36:04.223707'), Post('Blog 2', '2022-12-13 07:36:04.226693')]

# printing all the titles of all the blogs. , using for loop. 

>>> for post in user.posts:
...     print(post.title)
...
Blog 1
Blog 2
>>>

# queruing the posts. 

>>> post  = Post.query.first()
>>>
>>> post
Post('Blog 1', '2022-12-13 07:36:04.223707')

# now to get the id, who created this. post. 

>>> post.user_if
1

>>> post.author
User('john', 'john@gmail.com', 'default.jpg')
>>> db.drop_all()
>>> db.create_all()
>>> User.query.all()
[]
>>> Post.query.all()
[]


project structure :- 


2. put all the models User model class and Post model class in a separate file. called as models.py just next to flaskblog.py file.
models.py 


from datetime import datetime
from flaskblog import db
# these two imports have to be cut from flaskblog.py file and pasted at the top. 
# then cut both the classes User, and Post class from flaskblog.py file and paste it here in this file(models.py)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


3. in flaskblog.py file , now we will have to write a new import statement at the top to import the USer and Post models from the models.py file. 

flaskblog.py 
from models import User, Post



4  User authentication. 
 4.1 password encryption, 

 pip install flask-bcrypt 

initialize this inside the __init__.py file at the top . 

__init__.py 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


4.2 in register.html ., flash a message, saying that new user has been registered. and that can be done from the register route from the routes.py file. 
first import db and bcrypt at the top of the file. 

routes.py 

from flaskblog import app, db, bcrypt

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # generate a hash code for the password entered and convert it into string format using the utf-8 as the parameter inside the decode() function. 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # get the information about the user from the html form.
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashed_password)
        # adding this user to the database.
        db.session.add(user)
        # maknig the changes permanent in the database. 
        db.session.commit()
        # display a successful message for register ,by adding a success as the bootstrap classs name. 
        flash('Your account has been created! You are now able to log in', 'success')
        # after successfull registration lets bring the user directly to the login page. 
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# now the user can get registered in to the database. 
# but with only one problem. any one can register with the same username and same email again and again we need to restrict this from happeningn. 
if the username or email already exists , we should get a message to choose another one. 


4.3 making custome validation 

go the forms.py file and at the end of the RegistrationForm class . we can add the custome validation on the username and email field. 

first import the User model from the models.py file at the top of forms.py file. 



forms.py

from flaskblog.models import User
from wtforms.validators import ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # create an inbuilt function to validate the fields of the form. 
    def validate_username(self, username):
        # try to see if the user is already there in the database or not. 
        user = User.query.filter_by(username = username.data).first()
        # if the user with same username is already in the database. 
        if user:
            # then raise the error. statement saying to choose different username,
             # ValidationError, is a class name which needs to be imported from the wtforms.validators library at the top.
            raise ValidationError("Username already taken , please choose a different one.")
    
    # custome function to validate the email entered by the user. 
    def validate_email(self, email):
        # check if the email id exists in the database, if its there raise error message to choose another email id. 
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("Email id already taken , please choose a different one.")


5. making the login system. 

# now the registration system will be working just fine.
now we need to do the login system. for this we are going to need a library , called as flask-login. 
and the class we need from this package or module is LoginManager
which we will need to install using pip 

pip install flask-login

5.1 initialize the login system inside the __init__.py file . 

__init__.py 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin

login_manager = LoginManager(app)


5.2  now we need to add this functionality into the models of our application . inside the models. py file. 
first import the instance of the login_manager at the top of this file. 



models.py 
from flaskblog import db, login_manager

# now create a function here at the top to fetch the user from the database based on the user_id passed. 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# now we need one more class from flask_login module called as UserMixin() 
# which has its own functionalites to add to the login page login form. 

so we will pass this as the second arguemnt in the User() constructor , in the class creation. 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


5.3  now the last thing to do is to check in the database , the username and email are valid or not. 
and make the successful login ,and redirect them to the home page. of the application
so in routes.py , go to the login route/function and make the changes. 


routes.py 

from flask_login import login_user

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # first check if the email id is already in the database or not. 
        user = User.query.filter_by(email=form.email.data).first()
        # now if the email is there. then check for the password entered by the user matches with the password in the database table.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            
            #  so if the email and password is correct , we will use the inbuilt function , 
            # login_user() which we will have to import from the flask_login library/package. to make the login 
            # successful

            login_user(user, remember=form.remember.data)   # second argument is True or False. (remember me)
            
            # after successful login . lets redirect them to the next page. that is home page.
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # if the email and password is incorrect , login will be Unsuccessful,
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


5.3  now make the login and register link disabled if the user is already logged in , and enable only if they are logged out of the application.

now to check if the user is currently logged in . we can use the inbuilt funciton , called as current_user() from the flask_login library , which we will have to import at the top of the routes.py file. 

and redirect the user to home page. if he is logged in. 
and we will make this change in the login route as well as the register route. at the top . just after starting the function login() and register() , 

now if you are logged in and if you click on the login or register link at the top you will not see them working. 
you will automatically be navigated to the home page. 


routes.py

from flask_login import login_user, current_user

@app.route("/login", methods=['GET', 'POST'])
def login():
    # here will use the current_user() function to redirect him to home page if he is already logged in. 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # first check if the email id is already in the database or not. 
        user = User.query.filter_by(email=form.email.data).first()
        # now if the email is there. then check for the password entered by the user matches with the password in the database table.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            
            #  so if the email and password is correct , we will use the inbuilt function , 
            # login_user() which we will have to import from the flask_login library/package. to make the login 
            # successful

            login_user(user, remember=form.remember.data)   # second argument is True or False. (remember me)
            
            # after successful login . lets redirect them to the next page. that is home page.
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            # if the email and password is incorrect , login will be Unsuccessful,
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



5.4  now lets make the logout() route , function in this file for makeing the user logout and return back to the login page. 

routes.py 


from flask_login import login_user, current_user, logout_user

@app.route("/logout")
def logout():
    # we are going to use the inbuilt function called as logout_user() from the flask_login package
    logout_user()
    return redirect(url_for('home'))


5.5 now add the logout route inside the layout.html page. 


we will create a logout link in nav bar. of the applicaiton inside an if else condition. 

          <div class="collapse navbar-collapse" id="navbarToggle">
            <div class="navbar-nav mr-auto">
              <a class="nav-item nav-link" href="{{ url_for('home')}}">Home</a>
              <a class="nav-item nav-link" href="{{ url_for('about')}}">About</a>
            </div>
            <!-- Navbar Right Side -->
            <div class="navbar-nav">
              {% if current_user.is_authenticated %}
              <a class="nav-item nav-link" href="{{ url_for('account')}}">User-Account</a>
              <a class="nav-item nav-link" href="{{ url_for('logout')}}">Logout</a>
              {% else %}
              <a class="nav-item nav-link" href="{{ url_for('login')}}">Login</a>
              <a class="nav-item nav-link" href="{{ url_for('register')}}">Register</a>
              {% endif %}
            </div>
          </div>
        </div>
      </nav>
