
from flask import Flask, render_template, request, flash, session, url_for, \
    redirect, abort, g, make_response, send_from_directory
import sqlite3
import os

from flask_admin import Admin
from sqlalchemy.testing import db

from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, \
    logout_user
from werkzeug.utils import secure_filename


# postgresql
import psycopg2
import psycopg2.extras
import hashlib
from config import host, db_name, user, password

# конфигурация бд
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'dhjdkjnfuefjkdsnfsdjfds'
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
SECRET_KEY = 'dhjdkjnfuefjkdsnfsdjfds'
app.config['SECRET_KEY'] = 'FHSGGSDBGDRUIDNGHDYHFDGJKFDJHBF'
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
admin = Admin(app, name='My Admin Panel', template_mode='bootstrap4')

# максимальный размер файла который можно загрузить на сервер(1мБ)
MAX_CONTENT_LENGHT = 1024 * 1024

menu = [{'url': '/', 'title': 'Категории'},
        {'url': '/manufacturers ', 'title': 'Производители'},
        {'url': '/products  ', 'title': 'Продукты '},
        {'url': '/customers ', 'title': 'Клиенты'},
        {'url': '/orders ', 'title': 'Заказы'},
        {'url': '/reviews  ', 'title': 'Отзывы'}
        ]

#метод для подключения бд
def connect_db():
    connection = psycopg2.connect(host=host, user=user, password=password,
                                  database=db_name)
    connection.autocommit = True

    return connection

def get_db():
    # установка соединения
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

# закрытие соединения с бд
@app.teardown_appcontext
def close_db(error):
    # разрыв соединения
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None

#Устанавливаем соединение с БД перед выполнением запроса
@app.before_request
def before_request():
    """Устанавливаем соединение с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


# Добавляем обработчик для CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin',
                         'http://127.0.0.1:5000')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,POST,PUT,DELETE,OPTIONS')
    return response

#функция обрабатывающая сценарий перехода на страницу которая вызывает 404 ошибку
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', menu=menu)

#функция обработчик главноей страницы которая выводит список категорийй
@app.route("/")
def index():
    return render_template('index.html', menu=menu, klient=dbase.getCategory())

#функция обработчик страницы о конкретной категории принимает id категории(alias)
@app.route("/category/<alias>")
def ShowCategory(alias):
    res = dbase.getCategoryByID(alias)
    print(res)
    if not res["category_id"]:
        abort(404)
    return render_template('category_detail.html', menu=menu,
                           category_id=res["category_id"], name=res["name"])

#функция обработчик удаления категории
@app.route("/category/<user_id>/delete")
def DeleteCategory(user_id):
    try:
        print(user_id)
        res = dbase.DeleteCategory(user_id)
        if not res:
            pass

    except Exception as e:
        flash("Что-то пошло не так", "error")
    return render_template('category_delete.html', menu=menu)

#функция обработчик добавления категории
@app.route("/category_add", methods=['POST', 'GET'])
def addCategory():
    if request.method == "POST":
        if len(request.form['name']) > 1:
            res = dbase.addCategory(request.form['name'], )
            if not res:
                flash("Ошибка добавления категории", category='error')
            else:
                flash('Категория добавлена успешно', category="success")
        else:
            flash("Ошибка добавления категории", category='error')

    return render_template('category_add.html', menu=menu)

#функция обработчик  которая выводит список производителей
# Производители
@app.route("/manufacturers")
def manufacturers():
    return render_template('manufacturers.html', menu=menu,
                           klient=dbase.getManufacturers())

#функция обработчик  которая выводит конкретного производителя по id
@app.route("/manufacturers/<alias>")
def ShowManufacturers(alias):
    res = dbase.getManufacturersByID(alias)
    print(res)
    if not res["manufacturer_id"]:
        abort(404)
    return render_template('manufacturers_detail.html', menu=menu,
                           manufacturer_id=res["manufacturer_id"],
                           name=res["name"])

#функция обработчик удаления производителя по id
@app.route("/manufacturers/<user_id>/delete")
def DeleteManufacturers(user_id):
    try:
        print(user_id)
        res = dbase.DeleteManufacturers(user_id)
        if not res:
            pass

    except Exception as e:
        flash("Что-то пошло не так", "error")
    return render_template('manufacturers_delete.html', menu=menu)

#функция обработчик добавления производителя
@app.route("/manufacturers_add", methods=['POST', 'GET'])
def addManufacturers():
    if request.method == "POST":
        if len(request.form['name']) > 1:
            res = dbase.addManufacturers(request.form['name'], )
            if not res:
                flash("Ошибка добавления производителя", category='error')
            else:
                flash('Производитель добавлен успешно', category="success")
        else:
            flash("Ошибка добавления производителя", category='error')

    return render_template('manufacturers_add.html', menu=menu)

#функция обработчик  которая выводит список продуктов
# Продукты
@app.route("/products")
def products():
    return render_template('product.html', menu=menu,
                           klient=dbase.getProduct())

#функция обработчик  которая выводит конкретный продукт по id
@app.route("/products/<alias>")
def ShowProduct(alias):
    res = dbase.getProductByID(alias)
    print(res)
    category_id = res["category_id"]
    res2 = dbase.getCategoryByID(category_id)
    manufacturer_id = res["manufacturer_id"]
    res3 = dbase.getManufacturersByID(manufacturer_id)
    if not res["product_id"]:
        abort(404)
    return render_template('product_detail.html', menu=menu,
                           product_id=res["product_id"], name=res["name"],
                           price=res["price"],
                           category=res2["name"], manufacturer=res3["name"])

#функция обработчик удаления продукта по id
@app.route("/products/<user_id>/delete")
def DeleteProduct(user_id):
    try:
        print(user_id)
        res = dbase.DeleteProduct(user_id)
        if not res:
            pass

    except Exception as e:
        flash("Что-то пошло не так", "error")
    return render_template('product_delete.html', menu=menu)


#функция обработчик добавления продукта
@app.route("/product_add", methods=['POST', 'GET'])
def addProduct():
    if request.method == "POST":
        if len(request.form['name']) > 1 and len(
                request.form['price']) > 0 and len(
                request.form['category']) and len(request.form['man']):
            res = dbase.addProduct(request.form['name'], request.form['price'],
                                   request.form['category'],
                                   request.form['man'],)
            if not res:
                flash("Ошибка добавления продукта", category='error')
            else:
                flash('Продукт добавлен успешно', category="success")
        else:
            flash("Ошибка добавления продукта", category='error')

    return render_template('product_add.html', menu=menu)


#функция обработчик  которая выводит список клиентов
# Клиенты
@app.route("/customers")
def customers():
    return render_template('customers.html', menu=menu,
                           klient=dbase.getCustomers())

#функция обработчик  которая выводит конкретного клиента по id
@app.route("/customers/<alias>")
def ShowCustomers(alias):
    res = dbase.getCustomersByID(alias)
    print(res)
    if not res["customer_id"]:
        abort(404)
    return render_template('customer_detail.html', menu=menu,
                           customer_id=res["customer_id"], name=res["name"],email=res["email"])

#функция обработчик удаления клиента по id
@app.route("/customers/<user_id>/delete")
def DeleteCustomers(user_id):
    try:
        print(user_id)
        res = dbase.DeleteCustomers(user_id)
        if not res:
            pass

    except Exception as e:
        flash("Что-то пошло не так", "error")
    return render_template('customer_delete.html', menu=menu)

#функция обработчик добавления клиента
@app.route("/customer_add", methods=['POST', 'GET'])
def addCustomers():
    if request.method == "POST":
        if len(request.form['name']) > 1 and len(request.form['email']) >= 3:
            res = dbase.addCustomers(request.form['name'],request.form['email'])
            if not res:
                flash("Ошибка добавления клиента", category='error')
            else:
                flash('Клиент добавлен успешно', category="success")
        else:
            flash("Ошибка добавления клиента", category='error')

    return render_template('customer_add.html', menu=menu)
#функция обработчик  которая выводит список заказов
# Заказы
@app.route("/orders")
def orders():
    return render_template('order.html', menu=menu,
                           klient=dbase.getOrders())

#функция обработчик  которая выводит конкретный заказ по id
@app.route("/orders/<alias>")
def ShowOrder(alias):
    res = dbase.getOrderByID(alias)
    print(res)
    name = res["customer_id"]
    res2 = dbase.getCustomersByID(name)
    print(res2)
    if not res["order_id"]:
        abort(404)
    return render_template('order_detail.html', menu=menu,
                           order_id=res["order_id"], order_date=res["order_date"],customer=res2["name"])

#функция обработчик удаления заказа по id
@app.route("/orders/<user_id>/delete")
def DeleteOrders(user_id):
    try:
        print(user_id)
        res = dbase.DeleteOrder(user_id)
        if not res:
            pass

    except Exception as e:
        flash("Что-то пошло не так", "error")
    return render_template('order_delete.html', menu=menu)

#функция обработчик добавления заказа
@app.route("/order_add", methods=['POST', 'GET'])
def addOrders():
    if request.method == "POST":
        if len(request.form['name']) > 0 :
            res = dbase.addOrder(request.form['name'])
            if not res:
                flash("Ошибка добавления заказа", category='error')
            else:
                flash('Заказ добавлена успешно', category="success")
        else:
            flash("Ошибка добавления заказа", category='error')

    return render_template('reviews_add.html', menu=menu)



#функция обработчик  которая выводит список отзывов
#отзывы
@app.route("/reviews")
def reviews():
    return render_template('reviews.html', menu=menu,
                           klient=dbase.getReviews())

#функция обработчик  которая выводит конкретный отзыв  по id
@app.route("/reviews/<alias>")
def ShowReviews(alias):
    res = dbase.getReviewsByID(alias)
    print(res)
    name = res["product_id"]
    res2 = dbase.getCategoryByID(name)
    alias = res["product_id"]
    res3 = dbase.getCustomersByID(alias)
    print(res2)
    if not res["review_id"]:
        abort(404)
    return render_template('reviews_detail.html', menu=menu, review_id =res["review_id"],
                           rating =res["rating"], comment =res["comment"],review_date =res["review_date"],product_id =res2["name"],customer_id=res3["name"])
#функция обработчик добавления отзыва
@app.route("/review_add", methods=['POST', 'GET'])
def addReviews():
    if request.method == "POST":
        if len(request.form['name']) > 0 and len(
                request.form['email']) > 0 and len(
                request.form['rat']) > 0 and len(request.form['com']) > 0:
            res = dbase.addReviews(request.form['name'], request.form['email'],
                                 request.form['rat'], request.form['com'])
            if not res:
                flash("Ошибка добавления отзыва", category='error')
            else:
                flash('Отзыв добавлена успешно', category="success")
        else:
            flash("Ошибка добавления отзыва", category='error')

    return render_template('reviews_add.html', menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
