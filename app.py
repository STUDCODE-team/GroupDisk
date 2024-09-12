from flask import Flask
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == 'test@test.com' and password == 'test':
            return redirect(url_for('success'))
        else:
            return 'Неверный email или пароль'

    return render_template('auth.html')

# Страница успешного входа
@app.route('/success')
def success():
    return 'Вы успешно вошли!'

if __name__ == '__main__':
  app.run(debug=True)