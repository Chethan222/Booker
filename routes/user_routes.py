from flask import Blueprint,render_template,request,redirect,flash,make_response,g,url_for
import db.db_handler as db
from middlewares import authenticate
import json

main = Blueprint('main',__name__)

@main.route('/')
@main.route('/index')
@authenticate
def home():
    try:
        if(g.user):
            return render_template('home.html',user=g.user)
    except Exception as e:
        print("ERROR",e)
    return render_template('home.html')


@main.route('/register',methods=['POST','GET'])
@authenticate
def main_register():
    message = ''
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            phone = request.form['phone']
            
            user = db.getUserByEmail(email)
            if(len(user)>0):
                flash('Email address already exists.','sucess')
                return redirect('/register')
  
            sucess = db.create_user(name,email,password,phone)
            if(sucess):
                flash('Registration Sucessful.','sucess')
                return redirect('/register')
            flash('Registration failed! Phone number has been used!','error')
            return redirect('/register')
        except Exception as e:
            print(e)
            message = 'Something went wrong!'
    return render_template('register.html',message=message)

@main.route('/logout')
@authenticate
def logout():
    if(g.user):
        g.user = None
        res = make_response(redirect(url_for('.home')))
        res.delete_cookie('userId')
        res.set_cookie('userID', '', expires=0)
        return res
    return redirect('/')

@main.route('/login',methods=['POST', 'GET'])
@authenticate
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.login(email,password)

        if(user == 0):
            flash('Invalid email or password!')
            return redirect('/login')

        flash('Login Sucessful.')
        res = make_response(redirect(url_for('.home',user= json.dumps(user))))
        res.set_cookie('userID',str(user.get('id')),max_age=60*30)

        return res

    return render_template('login.html')


@main.route('/halls')
@authenticate
def halls():
    if(g.user):
        halls = db.get_halls()
        print(halls)
        return render_template('halls.html',halls=halls)
    return redirect('/login')

@main.route('/halls/book/<int:hall_id>')
@authenticate
def book_hall(hall_id):
    if(g.user):
        user_id = g.user.get('id')
        res = db.book_hall(user_id,hall_id)
        if(res):
            book_id = db.get_booking(user_id,hall_id)[0][0]
            return render_template('book.html',book_id=book_id)
        flash("Something went wrong! Couldn't book hall.")
        return redirect('/halls')
    return redirect('/login')

@main.route('/halls/about/<int:id>')
@authenticate
def about_hall(id):
    if(g.user):
        hall = db.get_hall(id)
        if(hall):
            return render_template('about.html',hall=hall[0])
        flash('No hall found!')
        redirect('/halls')
    return redirect('/login')

@main.route('/dashboard')
@authenticate
def dashboard():
    user = g.user
    if(user):
        return render_template('dashboard.html',user=user)
    return redirect('/login')


@main.route('/update/<int:id>',methods=['POST'])
@authenticate
def update_user(id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            phone = request.form['phone']
            try:
                about = request.form['about']
                image = request.form['profileImage']
            except Exception as e:
                print(e)

            db.update_user(name,email,password,phone,id)
            flash('Profile updated sucessfully.')
        except Exception as e:
            flash('Unable to update profile!')
            print(e)
    return redirect('/dashboard')

@main.route('/delete/<int:id>')
@authenticate
def delete_user(id):
    if request.method == 'POST':
        try:
            db.delete_user(id)
            flash('Profile deleted sucessfully')
        except Exception as e:
            flash('Unable to delete profile!')
            print(e)
    g.user = None
    res = make_response(redirect(url_for('.home')))
    res.delete_cookie('userId')
    res.set_cookie('userID', '', expires=0)
    return res
