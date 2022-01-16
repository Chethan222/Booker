from flask import Blueprint,render_template,request,redirect,flash,jsonify,make_response,url_for,g
import db.db_handler as db
from werkzeug.utils import secure_filename
import os
from middlewares import  authenticate, authenticateAdmin
from admin_credentials import ADMIN

admin = Blueprint('admin',__name__)

@admin.route('/admin/login',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        print(ADMIN.get('email'),ADMIN.get('password'))
        if(email == ADMIN.get('email')):
            if(password == ADMIN.get('password')):
                res = make_response(redirect(url_for('.admin_home')))
                res.set_cookie('adminID',str(ADMIN.get('id')),max_age=60*10)
                return res
        else:
            flash('Invalid Credentials!')
    return render_template('admin_login.html')

@admin.route('/admin/logout')
@authenticateAdmin
def admin_logout():
    g.admin = None
    res = make_response(redirect(url_for('.admin_home')))
    res.delete_cookie('adminID')
    res.set_cookie('adminId', '', expires=0)
    return res

@admin.route('/admin')
@authenticateAdmin
def admin_home():
    return render_template('admin.html')


@admin.route('/admin/halls/add',methods=['POST',])
@authenticateAdmin
def admin_add():
    if request.method == 'POST':
        
        try:
            name = request.form['name']
            place = request.form['place']
            description = request.form['description']
            price = request.form['price']
            file = request.files['hallImg']
            
            UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/images/')
            res = db.create_hall(name, place,description,price,secure_filename(file.filename))
            file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
            if(not res):
                flash('Unable to create hall data!')
                return redirect('/admin')   
            flash('New hall data created sucessfully!')
            return redirect('/admin') 
        except Exception as e:
            print("ERROR",e)
            flash('Unable to create hall data!')
        return redirect('/admin')


@admin.route('/admin/halls')
@authenticateAdmin
def admin_get_halls():
    halls = db.get_halls()
    if(len(halls)==0):
        return jsonify([])

    halls_ = []

    for hall in halls:
        halls_.append({
            'id':hall[0],
            'name':hall[1],
            'place':hall[2],
            'description':hall[3],
            'image':hall[4],
            'price':hall[5]
            })
    return jsonify(halls_)

@admin.route('/admin/users')
@authenticateAdmin
def admin_get_users():
    users = db.get_users()
    users_ = []
    if(len(users)==0):
        return jsonify([])
    for user in users:
        users_.append({
            'id':user[0],
            'email':user[1],
            'name':user[3],
            'phone':user[4],
            })
    return jsonify(users_)


@admin.route('/admin/halls/update/<int:id>',methods=['POST',])
@authenticateAdmin
def admin_update(id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            place = request.form['place']
            description = request.form['description']
            price = request.form['price']
            hallImage = request.files['hallImg']

            res = db.update_hall(id,name,place,description,price,secure_filename(hallImage.filename))
            if(res):
                flash('Hall Updated sucessfully!')
                return redirect('/admin')
            flash('Something went wrong! Unable to update data!')
            return redirect('/admin')
        except Exception as e:
            print(e)
            flash('Something went wrong! Unable to update data!')
        return redirect('/admin')


@admin.route('/admin/halls/delete/<int:id>',methods=['GET',])
@authenticateAdmin
def admin_delete_hall(id):
    res = db.delete_hall(id)
    if(res):
        flash('Hall data deleted sucessfully!')
    else:
        flash('Unable to delete hall data!')
    return redirect('/admin')

@admin.route('/admin/user/delete/<int:id>',methods=['GET',])
@authenticateAdmin
def admin_delete_user(id):
    res = db.delete_user(id)
    if(res):
        flash('User removed sucessfully!')
    else:
        flash('Unable to remove user!')
    return redirect('/admin')
