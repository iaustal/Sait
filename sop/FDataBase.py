import datetime

import re
import psycopg2.extras
from flask_login import current_user

from flask import url_for

#класс для работы с бд
class FDataBase:
    def __init__(self, db):
        self.__db = db
        #self.__cur = db.cursor()
        self.__cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    #получения всех категорий
    def getCategory(self):
        sql = """select * from categories"""

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            print(res)
            if res: return res
        except:
            print("Ошибка чтения из бд")
        return []

    # получения категории по id
    def getCategoryByID(self, alias):
        try:
            print('id', alias)
            self.__cur.execute(
                f"select * from categories  WHERE category_id  = '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except Exception as e:
            print("Ошибка получения категории из БД " + str(e))
        return (False, False)

    # добавление категории  принимает название категории
    def addCategory(self, name):
        try:
            self.__cur.execute(
                f"INSERT INTO categories(name) VALUES('{name}')")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления категории в БД " + str(e))
            return False

        return True

    # удаление категории по id
    def DeleteCategory(self, id):
        print('----')
        print(id)
        try:
            self.__cur.execute(f"delete from categories  where category_id ={id}")
            self.__db.commit()
        except Exception as e:
            print("Ошибка Удаления поста из БД " + str(e))
            return False

    # получение всех производителей
    def getManufacturers(self):
        sql = """select * from manufacturers """

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            print(res)
            if res: return res
        except:
            print("Ошибка чтения из бд")
        return []

    # получение  производителя по id
    def getManufacturersByID(self, alias):
        try:
            print('id', alias)
            self.__cur.execute(
                f"select * from manufacturers   WHERE manufacturer_id  = '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except Exception as e:
            print("Ошибка получения категории из БД " + str(e))
        return (False, False)

    # добавление производителя  принимает название производителя
    def addManufacturers(self, name):
        try:
            self.__cur.execute(
                f"INSERT INTO manufacturers(name) VALUES('{name}')")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления категории в БД " + str(e))
            return False

        return True
    #удаление производителя по id
    def DeleteManufacturers(self, id):
        print('----')
        print(id)
        try:
            self.__cur.execute(f"delete from manufacturers  where manufacturer_id ={id}")
            self.__db.commit()
        except Exception as e:
            print("Ошибка Удаления поста из БД " + str(e))
            return False
    #метод получения списка продуктов
    def getProduct(self):
        sql = """select * from products """

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            print(res)
            if res: return res
        except:
            print("Ошибка чтения из бд")
        return []

    # метод получения конкретного продукта по айди
    def getProductByID(self, alias):
        try:
            print('id', alias)
            self.__cur.execute(
                f"select * from products   WHERE product_id  = '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except Exception as e:
            print("Ошибка получения категории из БД " + str(e))
        return (False, False)
    #добавление продукта принимаеи название продукта,цена,айди категории и производителя
    def addProduct(self, name,price,category_id,manufacturer_id):
        try:
            self.__cur.execute(
                f"INSERT INTO products(name,price,category_id,manufacturer_id ) VALUES('{name}','{price}','{category_id}','{manufacturer_id}')")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления категории в БД " + str(e))
            return False

        return True
    #удаление продукта по айди
    def DeleteProduct(self, id):
        print('----')
        print(id)
        try:
            self.__cur.execute(
                f"delete from products  where product_id ={id}")
            self.__db.commit()
        except Exception as e:
            print("Ошибка Удаления поста из БД " + str(e))
            return False



    #получения списка всех пользователей
    def getCustomers(self):
        sql = """select * from customers  """

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            print(res)
            if res: return res
        except:
            print("Ошибка чтения из бд")
        return []

    #получения конкретного пользователя по айди
    def getCustomersByID(self, alias):
        try:
            print('id', alias)
            self.__cur.execute(
                f"select * from customers   WHERE customer_id  = '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except Exception as e:
            print("Ошибка получения категории из БД " + str(e))
        return (False, False)

    #добавление пользователя принимает имя и почту
    def addCustomers(self, name,email):
        try:
            self.__cur.execute(
                f"INSERT INTO customers(name,email ) VALUES('{name}','{email}')")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления категории в БД " + str(e))
            return False

        return True

    #удаление пользователя по айди
    def DeleteCustomers(self, id):
        print('----')
        print(id)
        try:
            self.__cur.execute(
                f"delete from customers  where customer_id ={id}")
            self.__db.commit()
        except Exception as e:
            print("Ошибка Удаления поста из БД " + str(e))
            return False

    #вывод всех заказов
#----------------------------------------------
    def getOrders(self):
        sql = """select * from orders """

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            print(res)
            if res: return res
        except:
            print("Ошибка чтения из бд")
        return []

    #вывод заказа по айди
    def getOrderByID(self, alias):
        try:
            print('id', alias)
            self.__cur.execute(
                f"select * from orders    WHERE order_id  = '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except Exception as e:
            print("Ошибка получения категории из БД " + str(e))
        return (False, False)

    #добавление закаха принимает его название
    def addOrder(self, name):
        try:
            self.__cur.execute(
                f"INSERT INTO orders(customer_id) VALUES('{name}')")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления категории в БД " + str(e))
            return False

        return True

    #удаление заказа
    def DeleteOrder(self, id):
        print('----')
        print(id)
        try:
            self.__cur.execute(
                f"delete from orders  where order_id ={id}")
            self.__db.commit()
        except Exception as e:
            print("Ошибка Удаления поста из БД " + str(e))
            return False

#--------------------------

    #получение всех отзывов
    def getReviews(self):
        sql = """select * from reviews"""

        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            print(res)
            if res: return res
        except:
            print("Ошибка чтения из бд")
        return []

    #получение отзыва по айди
    def getReviewsByID(self, alias):
        try:
            print('id', alias)
            self.__cur.execute(
                f"select * from reviews  WHERE review_id  = '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except Exception as e:
            print("Ошибка получения категории из БД " + str(e))
        return (False, False)

    #добавление отзыва
    def addReviews(self, product_id,customer_id,rating,comment):
        try:
            self.__cur.execute(
                f"INSERT INTO reviews(product_id,customer_id,rating,comment) VALUES('{product_id}','{customer_id}','{rating}','{comment}')")
            self.__db.commit()
        except Exception as e:
            print("Ошибка добавления категории в БД " + str(e))
            return False

        return True
