from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Auth, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Не забудьте установить секретный ключ для сессий
db.init_app(app)


@app.before_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth'))  # Если пользователь не авторизован, перенаправляем на страницу логина
    return render_template('main.html')  # Главная страница после входа


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
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Пожалуйста, введите имя пользователя и пароль"

        user = Auth.query.filter_by(username=username).first()

        if user and check_password_hash(auth.password, password):
            session['auth_id'] = auth.id
            return redirect(url_for('main.html'))  # Перенаправление на главную страницу
        else:
            return "Неверное имя пользователя или пароль"
    return render_template('auth.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Проверка, чтобы пользователь с таким именем уже не существовал
        existing_user = Auth.query.filter_by(username=username).first()
        if existing_user:
            return "Пользователь с таким именем уже существует"

        new_user = Auth(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth'))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)