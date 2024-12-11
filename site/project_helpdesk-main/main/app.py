from flask import Flask, render_template, flash, request, redirect, url_for, session
from models import db, Auth, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db.init_app(app)


@app.before_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    if 'auth_id' not in session:
        return redirect(url_for('auth'))
    return render_template('main.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/request')
def request_page():
    return render_template('request.html')


@app.route('/tickets')
def tickets():
    return render_template('tickets.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Auth.query.filter_by(username=username, password = password).first()
        if user:
            session['auth_id'] = user.id
            return redirect(url_for('index'))
        else:
            return "Неверное имя пользователя или пароль"
    return render_template('auth.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = Auth.query.filter_by(username=username).first()
        if user:
            return "Пользователь с таким именем уже существует"

        new_user = Auth(username=username,email=email , password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Зарегистрировался')

        return redirect(url_for('auth'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run()