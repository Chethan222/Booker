from flask import Flask
from settings import Config
from routes.user_routes import main
from routes.admin_routes import admin
from db.db_handler import db
import db.db_handler as dbUtilts


#Creating the app
app = Flask(__name__)

#Making necessary configurations
app.config.from_object(Config)


app.register_blueprint(main)
app.register_blueprint(admin)

db.init_app(app)

created = 0
# Database creation for the first time
# if not created :
#     with app.app_context():
#         created = 1
#         dbUtilts.create_hall_table()
#         dbUtilts.create_user_table()
#         dbUtilts.create_booking_table()

if __name__ == '__main__':
    app.debug=True
    app.run()

