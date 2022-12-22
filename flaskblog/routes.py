from flaskblog.models import User,Post
from flask import render_template, url_for, redirect, flash,request,abort
#importing db  for connecting routes to the datbase and instance variable bcrypt which is created in the __init__.py for decrypting password
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm,UpdateAccountForm, PostForm
from flask_login import login_user, current_user,logout_user, login_required,UserMixin
import secrets
import os
from PIL import Image


@app.route("/")

@app.route("/home")
def home():
    # get all the post from the database. 
    posts = Post.query.all()
    return render_template('home.html', posts = posts)

    # now you will be able to add new posts and it will get shown in the home page. and this we would have fetched from the database. 


@app.route("/about")
def about():
    return render_template('about.html', title='About')

# function to save the profile picture. 
def save_picture(form_picture):
    # change the name of the image to a simple name as soon as they will upload a image. this can be done by importing secrets module at the top from python directly , by writing.    import secrets. and using it here. 
    random_hex = secrets.token_hex(8)
    # now we will use the os moduel from python to save the file in the same extentions as the image extention. so impor os library and use the function. 
    # this function returns 2 values image file without the extension and second is the extension itself. 
    _ , f_ext = os.path.splitext(form_picture.filename)  # we dont require the file name in this line so we put it as _ underscore. 
    # f_name , f_ext = os.path.splitext(form_picture.filename)
    # we need the file name in this next line. 
    picture_fn = random_hex + f_ext
    # now we will store this image uploaded into the static folders profile_pics folder. 
    picture_path = os.path.join(app.root_path , "static/profile_pics", picture_fn)
    # now we will save that picture using the form_picture variable using the save() function. at the picture path that we just created. 
    # resize the image before saving. 
    output_size = (125, 125)
    # get the image from the form. 
    i = Image.open(form_picture)
    # now set the thumbnail of the image to the output_size which we have choosen.  
    i.thumbnail(output_size)
    # now save this i resized image. into the folder location. 
    i.save(picture_path)
    # finally we will return the pictures file name, which was uploaded by the user. 
    return picture_fn


@app.route("/profile",methods=['POST', 'GET'])
@login_required
def profile():
   # make the instance of the UpdateAccountForm and pass that form into the account.html template. 
    form = UpdateAccountForm()
    # check if the form is valid on submission .
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file=picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account details were successfully updated.", "success")
        # after updation we will redirect them to the account page. 
        return redirect(url_for("profile"))
    elif request.method == "GET":
        # this is to populate the form by the current users data as soon as they come to the account update page. 
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static" , filename = "profile_pics/" + current_user.image_file)
    # pass this image_file variable into the accont.html template
    return render_template("profile.html", title = "User Profile" , image_file = image_file , form = form)




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

# function to save the profile picture.
def save_post_picture(form_picture):
    # change the name of the image to a simple name as soon as they will upload a image. this can be done by importing secrets module at the top from python directly , by writing.    import secrets. and using it here.
    random_hex = secrets.token_hex(8)
    # now we will use the os moduel from python to save the file in the same extentions as the image extention. so impor os library and use the function.
    # this function returns 2 values image file without the extension and second is the extension itself.
    _ , f_ext = os.path.splitext(form_picture.filename)  # we dont require the file name in this line so we put it as _ underscore.
    # f_name , f_ext = os.path.splitext(form_picture.filename)
    # we need the file name in this next line.
    picture_fn = random_hex + f_ext
    # now we will store this image uploaded into the static folders profile_pics folder.
    picture_path = os.path.join(app.root_path , "static/post_pics", picture_fn)
    # now we will save that picture using the form_picture variable using the save() function. at the picture path that we just created.
    # resize the image before saving.
    output_size = (125, 125)
    # get the image from the form.
    i = Image.open(form_picture)
    # now set the thumbnail of the image to the output_size which we have choosen.
    i.thumbnail(output_size)
    # now save this i resized image. into the folder location.
    i.save(picture_path)
    # finally we will return the pictures file name, which was uploaded by the user.
    return picture_fn

# now make an instance of the PostForm class inside the route.py file  inside the new_post() method or route and send it to the create_post.html page. as a variable. also mention the allowed methods for this route, POSt and GET

# function to create new post / add new post 
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # if form.post_image.data:
        #     picture_file = save_post_picture(form.post_image.data)
        #     current_user.post_id.post_image=picture_file
        post = Post(title=form.title.data, content=form.content.data,post_image=form.post_image.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


# now show this form inside the create_post.html page.


# now we will make a route, to show the specific post , by fetching it by its id.
# fetching the post by its id.

@app.route("/post/<int:post_id>")
def post(post_id):
    # we can get the post by its id using the get() function.
    post = Post.query.get_or_404(post_id)
    return render_template('post.html' , title = post.title, post = post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# we have to logged in to update the post so we need the login_required decorator
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # we have to make sure the person who wrote the post only should get to update it. not any one else.
    if post.author != current_user:
        abort(403)        # import the about() function from flask library. 
    # now to show the update form. from where we can update the title and content of the post.
    form = PostForm()
    # if the form is successfully validated on clicking the submit button.
    if form.validate_on_submit():
        # if form.post_image.data:
        #     picture_file = save_post_picture(form.image_file.data)
        #     current_user.post_id.post_image=picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        # after successful update we will redirect the user to the udated  post page.
        # post_image = url_for("static" , filename = "post_pics/" + current_user.post.post_image)
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        # this fetches the post alredy in the database, which we will get it from method GET
        form.title.data = post.title
        form.content.data = post.content
        form.post_image.data = post.post_image
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


# now lets create the delete route for our application . 

# route to delete the post. and we will acceept only post request for deleting post. 
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    # deleting the post by its post_id. 
    post = Post.query.get_or_404(post_id)
    # only the person who wrote the post gets to delete it. 
    if post.author != current_user:
        abort(403)       # this will show forbidden message if the post doesnt belong to the user. who wrote the post. 
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    # after successfull deletion make the user come to the home page.
    return redirect(url_for('home'))


