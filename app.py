import os
from flask import Flask, render_template, request, flash, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Путь к файлу с данными заявок
DATA_FILE = 'application.json'

# Загрузка существующих заявок из файла
try:
    with open(DATA_FILE, 'r') as file:
        applications = json.load(file)
except FileNotFoundError:
    applications = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        email = request.form.get('email')

        # Проверка заполненности всех полей
        if not all([name, description, email]):
            flash('Пожалуйста, заполните все поля.', 'error')
            return redirect(url_for('index'))

        # Регистрация новой заявки
        application_id = len(applications) + 1
        new_application = {
            'id': application_id,
            'name': name,
            'description': description,
            'email': email
        }
        applications.append(new_application)

        # Сохранение новых данных в файл
        with open(DATA_FILE, 'w') as file:
            json.dump(applications, file, indent=4)

        flash('Заявка успешно зарегистрирована!', 'success')
        return redirect(url_for('success', application_id=application_id))

    return render_template('index.html')

@app.route('/success/<int:application_id>')
def success(application_id):
    application = next((a for a in applications if a['id'] == application_id), None)
    if not application:
        abort(404)
    return render_template('success.html', application=application)

if __name__ == '__main__':
    app.run(debug=True)