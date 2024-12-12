from flask import Flask, render_template, flash, request, redirect, url_for, session, jsonify
from models import db, Auth, User, Role, Task, Status
import datetime as DT


app = Flask(__name__)

tickets = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db.init_app(app)

'''@app.route('/add_roles')
def add_roles():
    #admin_role = Role(name="admin")
    #user_role = Role(name="user")
    executor_role = Role(name = "executor")

    #db.session.add(admin_role)
    #db.session.add(user_role)
    db.session.add(executor_role)

    db.session.commit()
    

    return "Роли добавлены в базу данных!"'''

@app.route('/')
def index():
    if 'auth_id' not in session:
        return redirect(url_for('auth'))
    return render_template('main.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/request', methods=['GET', 'POST'])
def request_page():
    if request.method == 'POST':
        name_client = request.form['name_client']
        email = request.form['email']
        subject = request.form['subject']
        description = request.form['description']
        type = request.form['type']

        # Создаем новую задачу
        new_ticket = Task(
            name_client=name_client,
            email=email,
            subject=subject,
            description=description,
            type=type,
            beg_date=DT.datetime.utcnow()
        )

        # Добавляем заявку в базу данных
        db.session.add(new_ticket)
        db.session.commit()

        flash('Заявка успешно отправлена!')
        return redirect(url_for('tickets'))  # Перенаправляем на страницу с заявками

    return render_template('request.html')


@app.route('/tickets')
def tickets():
    tickets_list = Task.query.all()  # Получаем все заявки
    return render_template('tickets.html', tickets=tickets_list)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Auth.query.filter_by(username=username, password = password).first()
        if user:
            session['auth_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            session['role_id'] = user.role_id
            return redirect(url_for('index'))
        else:
            return "Неверное имя пользователя или пароль"
    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.pop('auth_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


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
        user_role = Role.query.filter_by(name="user").first()  # Поиск роли 'user'
        new_user.role = user_role  # Назначаем роль пользователю
        db.session.add(new_user)
        db.session.commit()
        flash('Зарегистрировался')

        return redirect(url_for('auth'))
    return render_template('register.html')

@app.route('/profile')
def profile():
    # user = Auth.query.filter_by(id = session['auth_id']).first()

    return render_template('profile.html' )

@app.route('/assign_role/<int:user_id>/<role_name>', methods=['GET'])
def assign_role(user_id, role_name):
    user = Auth.query.get(user_id)
    if user:
        user.assign_role(role_name)
        return f"Роль '{role_name}' назначена пользователю {user.username}."
    return "Пользователь не найден", 404

@app.route('/remove_role/<int:user_id>', methods=['GET'])
def remove_role(user_id):
    user = Auth.query.get(user_id)
    if user:
        user.remove_role()
        return f"Роль снята с пользователя {user.username}."
    return "Пользователь не найден", 404

@app.route('/admin_page')
def admin_page():
    # user_id = session.get('user_id')
    # user = Auth.query.get(user_id)

    if session['username'] and session.get('role_id') == 1:
        return "Добро пожаловать в админ-панель"
    else:
        return "У вас нет доступа к этой странице", 403
    
@app.route('/update_ticket_status', methods=['POST'])
def update_ticket_status():
    ticket_id = request.form.get('ticket_id')
    status_color = request.form.get('status_color')
    
    ticket = Task.query.get(ticket_id)
    if ticket:
        status = Status.query.filter_by(color=status_color).first()
        if status:
            ticket.status = status  # Update the status relationship
            db.session.commit()
            return jsonify({"message": "Status updated successfully"})
        return jsonify({"error": "Status not found"}), 404
    return jsonify({"error": "Ticket not found"}), 404

@app.route('/get_ticket_data')
def get_ticket_data():
    tickets = Task.query.all()  # Or add filters as per your needs
    data = []
    for ticket in tickets:
        data.append({
            'id': ticket.id,
            'name_client': ticket.name_client,
            'email': ticket.email,
            'subject': ticket.subject,
            'type': ticket.type,
            'beg_date': ticket.beg_date,
            'status': ticket.status.name if ticket.status else 'Не определен',
        })
    return jsonify(data)

@app.before_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)