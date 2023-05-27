from flask import Flask, render_template, request, url_for, flash, session, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfsfdfsdgsdgfsdfeweweewqqgeeryetyert3rregtreybdfgsf'

menu = [
    {'name': 'Главная', 'url': '/'},
    {'name': 'Установка', 'url': 'install-flask'},
    {'name': 'Первое приложение', 'url': 'first-app'},
    {'name': 'Обратная связь', 'url': 'contacts'},
    {'name': 'Авторизация', 'url': 'login'}
]


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'Serhii' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    context = {
        'title': 'Авторизация',
        'menu': menu
    }

    return render_template('login.html', context=context)


@app.errorhandler(404)
def pageNotFound(error):
    context = {
        'title': 'Страница не найдена',
        'menu': menu
    }
    return render_template('page404.html', context=context)


@app.route("/")
def index():
    context = {
        'title': 'Главная страница',
        'menu': menu
    }
    return render_template('index.html', context=context)


@app.route("/about")
def about():
    context = {
        'title': 'Сторінка про нас',
        'menu': menu
    }
    return render_template('about.html', context=context)


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(404)
    return f'Пользователь {username}'


@app.route('/contacts', methods=['POST', 'GET'])
def contacts():
    if request.method == 'POST':
        if len(request.form['email']) > 2:
            flash('Сообщение отправлено', category='alert-success')
        else:
            flash('Что то пошло не так', category='alert-danger')

    context = {
        'title': 'Обратная связь',
        'menu': menu
    }
    return render_template('contacts.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
