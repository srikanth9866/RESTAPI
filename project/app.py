from flask import Flask
from auth import auth_blueprint
from models import db

app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

db.init_app(app)

# Register blueprints
app.register_blueprint(auth_blueprint)

@app.route('/')
def home():
    return "Flask app is running!", 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database is created before running the app
    app.run(debug=True)

