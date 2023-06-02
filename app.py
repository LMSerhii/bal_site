import os.path
import sqlite3

from flask import Flask, render_template, request, url_for, flash, session, redirect, abort, g

from FDataBase import FDataBase

# Configuration
DATABASE = '/tmp/balsite.db'
DEBUG = 'True'
SECRET_KEY = 'dfsfdfsdgsdgfsdfeweweewqqgeeryetyert3rregtreybdfgsf'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'balsite.db')))


def connect_db():
    """Функция соединения с базой данных"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """ Вспомогательная функция для создания с таблиц БД """
    db = connect_db()
    with app.open_resource('sq_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """ Соединение с БД, если оно еще не установлено """
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# menu = [
#     {'name': 'Главная', 'url': '/'},
#     {'name': 'Установка', 'url': 'install-flask'},
#     {'name': 'Первое приложение', 'url': 'first-app'},
#     {'name': 'Обратная связь', 'url': 'contacts'},
#     {'name': 'Авторизация', 'url': 'login'}
# ]

menu = []


@app.teardown_appcontext
def close_db(error):
    """ Закрываем соединение с БД, если оно было установлено """
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/login', methods=['POST', 'GET'])
def login():
    db = get_db()
    dbase = FDataBase(db)
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'Serhii' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    context = {
        'title': 'Авторизация',
        'menu': dbase.get_menu()
    }

    return render_template('login.html', context=context)


@app.errorhandler(404)
def pageNotFound(error):
    db = get_db()
    dbase = FDataBase(db)
    context = {
        'title': 'Страница не найдена',
        'menu': dbase.get_menu()
    }
    return render_template('page404.html', context=context)


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    context = {
        'title': 'Главная страница',
        'menu': dbase.get_menu(),
        'posts': dbase.getPostsAnonce()
    }
    return render_template('index.html', context=context)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    db = get_db()
    dbase = FDataBase(db)
    post_title, post_text = dbase.getPost(post_id)
    if not post_title:
        abort(404)
    context = {
        'title': post_title,
        'menu': dbase.get_menu(),
        'post_title': post_title,
        'post_text': post_text
    }
    return render_template('post.html', context=context)


@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['title']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['title'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='alert-danger')
            else:
                flash('Статья добавлена успешно', category='alert-success')
        else:
            flash('Ошибка добавления статьи', category='alert-danger')

    context = {
        'title': 'Добавление поста',
        'menu': dbase.get_menu()

    }
    return render_template('add_post.html', context=context)


@app.route("/about")
def about():
    db = get_db()
    dbase = FDataBase(db)
    context = {
        'title': 'Сторінка про нас',
        'menu': dbase.get_menu()
    }
    return render_template('about.html', context=context)


@app.route('/profile/<username>')
def profile(username):
    db = get_db()
    dbase = FDataBase(db)
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(404)
    return f'Пользователь {username}'


@app.route('/contacts', methods=['POST', 'GET'])
def contacts():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['email']) > 2:
            flash('Сообщение отправлено', category='alert-success')
        else:
            flash('Что то пошло не так', category='alert-danger')

    context = {
        'title': 'Обратная связь',
        'menu': dbase.get_menu()
    }
    return render_template('contacts.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
