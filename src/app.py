from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['userEmail']
        user_password = request.form['userPassword']
        user = User(0, user_email, user_password)
        logged_user = ModelUser.login(db, user)
        if logged_user:
            if logged_user.password:
                login_user(logged_user)
                flash("Inicio de sesion exitoso", "success")
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta", "error")
        else:
            flash("Usuario no encontrado", "error")
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['userName']
        user_lastname = request.form['userLastName']
        user_email = request.form['userEmail']
        user_password = request.form['userPassword']
        user_phone = request.form['userPhone']
        user_address = request.form['userAddress']
        
        new_user = User(0, user_email, user_password, user_name, user_lastname, user_phone, user_address)
        
        if ModelUser.register(db, new_user):
            flash("Te registraste correctamente", "success")
            return redirect(url_for('login'))
        else:
            flash("Error al registrarse", "error")
    
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('index.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)

# from flask import Flask, render_template, request

# from config import config

# app = Flask(__name__)

# @app.route('/')
# def login():
#     if request.method=='POST':
#         print(request.form['userEmail'])
#         print(request.form['userPassword'])
#         print(request.form['userName'])
#         print(request.form['userName'])
#         print(request.form['userName'])
#         print(request.form['userName'])
        
#         return render_template('auth/login.html')
#     else:
#         return render_template('auth/login.html')


# if __name__ == '__main__':
#     app.config.from_object(config['development'])
#     app.run()
    