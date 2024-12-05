from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/request')
def request():
    return render_template('request.html')

@app.route('/tickets')
def tickets():
    return render_template('tickets.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

if __name__ == '__main__':
    app.run(debug=True)