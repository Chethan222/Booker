from flask_sqlalchemy import SQLAlchemy
from matplotlib.style import use
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

def getData(cur):
    return [i for i in cur]

#Creating table

def create_hall_table():
    db.engine.execute("""CREATE TABLE halls(hall_id INTEGER NOT NULL,hall_name VARCHAR(120),hall_place VARCHAR(50),hall_description VARCHAR(320),hall_image VARCHAR(50),hall_price FLOAT,PRIMARY KEY (hall_id),UNIQUE (hall_name),UNIQUE (hall_image))""")


def create_user_table():
    db.engine.execute("""CREATE TABLE users(user_id INTEGER NOT NULL,user_email VARCHAR(120) NOT NULL,user_password VARCHAR(18) NOT NULL,user_name VARCHAR(25) NOT NULL,user_phone VARCHAR(10) NOT NULL,PRIMARY KEY (user_id),UNIQUE (user_email),UNIQUE (user_phone))""")

def create_booking_table():
    db.engine.execute("""CREATE TABLE bookings(book_id INTEGER NOT NULL,user_id INTEGER NOT NULL,hall_id INTEGER NOT NULL,PRIMARY KEY (book_id),FOREIGN KEY(user_id) REFERENCES users(user_id),FOREIGN KEY(hall_id) REFERENCES halls(hall_id))""")


########################## User #########################################

def create_user(name,email,password,phone):

    try:
        #Hashing password
        hashedPassword = generate_password_hash(password, method='sha256')
        db.engine.execute("INSERT INTO users(user_name,user_email,user_password,user_phone) VALUES(?,?,?,?)",(name,email,hashedPassword,phone))
    except Exception as e:
        print(e)
        return 0
    return 1
    

def update_user(name,email,password,phone,id):
    try:
        db.engine.execute("UPDATE  users SET user_name = ?,user_email = ?,user_password = ?,user_phone = ? WHERE user_id = ?",(name,email,password,phone,id))
    except Exception as e:
        print(e)
        return 0
    return 1


def search_user(name='',email='',phone=''):
    result = db.engine.execute("SELECT * FROM users WHERE user_name = ? OR user_email = ? OR user_phone = ?",(name,email,phone))
    return getData(result)
  
def login(email,password):
    user = getUserByEmail(email)
    if(len(user)>0):
        if check_password_hash(user[0].user_password, password):
            user_ = {
                'id':user[0][0],
                'email':user[0][1],
                'name':user[0][3],
                'phone':user[0][4],
                }
            return user_
    return 0



def getUserByEmail(email):
    result = db.engine.execute("SELECT * FROM users WHERE user_email = ?",(email))
    return getData(result)

def getUserById(id):
    result = db.engine.execute("SELECT * FROM users WHERE user_id = ?",(id))
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
    result = db.engine.execute("SELECT * FROM users WHERE user_id = ?",(id))
    user = getData(result)
    if(len(user)== 0 ):
        return 0
    return 1
  

def get_users():
    result = db.engine.execute("SELECT * FROM users")
    return getData(result)

def delete_user(id):
    try:
        db.engine.execute("DELETE FROM users WHERE user_id = ?",(id,))
    except Exception as e:
        print(e)
        return 0
    return 1

############################# Halls ####################################

def create_hall(name,place,description,price,image):
    try:
        db.engine.execute("INSERT INTO halls(hall_name,hall_place,hall_description,hall_price,hall_image) VALUES(?,?,?,?,?)",(name,place,description,price,image))
    except Exception as e:
        print(e)
        return 0
    return 1

def update_hall(id,name,place,description,price,image):
    try:
        db.engine.execute("UPDATE  halls SET hall_name = ?,hall_place = ?,hall_description = ?,hall_price = ?,hall_image=? WHERE hall_id = ?",(name,place,description,price,image,id))
    except Exception as e:
        return 0
    return 1

def delete_hall(id):
    try:
        db.engine.execute("DELETE FROM halls WHERE hall_id = ?",(id,))
    except Exception as e:
        print(e)
        return 0
    return 1

 
def get_hall(id):
    result = db.engine.execute("SELECT * FROM halls WHERE hall_id = ?",(id))
    return getData(result)
  
def search_user(name='',place='',description='',price=''):
    result = db.engine.execute("SELECT * FROM halls WHERE hall_name = ? OR hall_place = ? OR hall_description OR hall_price = ?",(name,place,description,price))
    return getData(result)
  

def get_halls():
    result = db.engine.execute("SELECT * FROM halls")
    halls_ =  getData(result)
    halls = []
    for hall in halls_:
        halls.append({
            'id':hall[0],
            'name':hall[1],
            'place':hall[2],
            'description':hall[3],
            'image':hall[4],
            'price':hall[5]
            })
    return halls
    
def delete_hall(id):
    try:
        db.engine.execute("DELETE FROM halls WHERE hall_id = ?",(id,))
    except Exception as e:
        print(e)
        return 0
    return 1

##################################### Bookings ############################################

def book_hall(user_id,hall_id):
    try:
        db.engine.execute("INSERT INTO bookings(user_id,hall_id) VALUES(?,?)",(user_id,hall_id))
        return 1
    except Exception as e:
        print(e)
        return 0

def get_booking(user_id,hall_id):
    result = db.engine.execute("SELECT book_id FROM bookings WHERE user_id = ? AND hall_id = ?",(user_id,hall_id))
    return getData(result)
    
def get_bookings():
    result = db.engine.execute("SELECT * FROM bookings")
    return getData(result)
