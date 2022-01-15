from functools import wraps
from flask import request,g,redirect
from matplotlib.style import use
import db.db_handler as db
from werkzeug.datastructures import MultiDict
from admin_credentials import ADMIN 

def authenticate(func):
        @wraps(func)
        def __home_decorator(*args, **kwargs):
            userId = request.cookies.get('userID')
            user = db.getUserById(userId)
            print("USER",user)
            if(not userId or len(user)== 0):
               g.user = None
            g.user = user
            result = func(*args, **kwargs)
            return result
        return __home_decorator

def authenticateAdmin(func):
    @wraps(func)
    def __home_decorator(*args, **kwargs):
        userId = request.cookies.get('adminID')
        
        if(not userId):
            return redirect('/admin/login')
        if(not(userId == ADMIN.get('id'))):
            return redirect('/admin/login')
        g.admin = True

        result = func(*args, **kwargs)
        return result
    return __home_decorator
