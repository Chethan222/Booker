from flask_sqlalchemy import SQLAlchemy
from matplotlib.style import use
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

def getData(cur):
    return [i for i in cur]

#Creating table

def create_hall_table():
    db.engine.execute("""CREATE TABLE halls(id INTEGER NOT NULL,name VARCHAR(120),place VARCHAR(50),description VARCHAR(320),image VARCHAR(50),price FLOAT,PRIMARY KEY (id),UNIQUE (name),UNIQUE (image))""")


def create_user_table():
    db.engine.execute("""CREATE TABLE users(id INTEGER NOT NULL,email VARCHAR(120) NOT NULL,password VARCHAR(18) NOT NULL,name VARCHAR(25) NOT NULL,phone VARCHAR(10) NOT NULL,PRIMARY KEY (id),UNIQUE (email),UNIQUE (phone))""")



########################## User #########################################

def create_user(name,email,password,phone):

    try:
        #Hashing password
        hashedPassword = generate_password_hash(password, method='sha256')
        db.engine.execute("INSERT INTO users(name,email,password,phone) VALUES(?,?,?,?)",(name,email,hashedPassword,phone))
    except Exception as e:
        print(e)
        return 0
    return 1
    

def update_user(name,email,password,phone,id):
    try:
        db.engine.execute("UPDATE  users SET name = ?,email = ?,password = ?,phone = ? WHERE id = ?",(name,email,password,phone,id))
    except Exception as e:
        print(e)
        return 0
    return 1


def search_user(name='',email='',phone=''):
    result = db.engine.execute("SELECT * FROM users WHERE name = ? OR email = ? OR phone = ?",(name,email,phone))
    return getData(result)
  
def login(email,password):
    user = getUserByEmail(email)
    if(len(user)>0):
        if check_password_hash(user[0].password, password):
            user_ = {
                'id':user[0][0],
                'email':user[0][1],
                'name':user[0][3],
                'phone':user[0][4],
                }
            return user_
    return 0



def getUserByEmail(email):
    result = db.engine.execute("SELECT * FROM users WHERE email = ?",(email))
    return getData(result)

def getUserById(id):
    result = db.engine.execute("SELECT * FROM users WHERE id = ?",(id))
    user = getData(result)
    if(len(user)>0):
        user_ = {
                    'id':user[0][0],
                    'email':user[0][1],
                    'name':user[0][3],
                    'phone':user[0][4],
                    }
        return user_
    return user
    
def get_user(id):
    result = db.engine.execute("SELECT * FROM users WHERE id = ?",(id))
    user = getData(result)
    if(len(user)== 0 ):
        return 0
    return 1
  

def get_users():
    result = db.engine.execute("SELECT * FROM users")
    return getData(result)

def delete_user(id):
    try:
        db.engine.execute("DELETE FROM users WHERE id = ?",(id,))
    except Exception as e:
        print(e)
        return 0
    return 1

############################# Halls ####################################

def create_hall(name,place,description,price,image):
    try:
        db.engine.execute("INSERT INTO halls(name,place,description,price,image) VALUES(?,?,?,?,?)",(name,place,description,price,image))
    except Exception as e:
        print(e)
        return 0
    return 1

def update_hall(id,name,place,description,price,image):
    try:
        db.engine.execute("UPDATE  halls SET name = ?,place = ?,description = ?,price = ?,image=? WHERE id = ?",(name,place,description,price,image,id))
    except Exception as e:
        return 0
    return 1

def delete_hall(id):
    try:
        db.engine.execute("DELETE FROM halls WHERE id = ?",(id,))
    except Exception as e:
        print(e)
        return 0
    return 1

 
def get_hall(id):
    result = db.engine.execute("SELECT * FROM halls WHERE id = ?",(id))
    return getData(result)
  
def search_user(name='',place='',description='',price=''):
    result = db.engine.execute("SELECT * FROM halls WHERE name = ? OR place = ? OR description OR price = ?",(name,place,description,price))
    return getData(result)
  

def get_halls():
    result = db.engine.execute("SELECT * FROM halls")
    return getData(result)

def delete_hall(id):
    try:
        db.engine.execute("DELETE FROM halls WHERE id = ?",(id,))
    except Exception as e:
        print(e)
        return 0
    return 1
