import os

from werkzeug.serving import run_simple
from mysql.connector import connect, Error
from time import sleep

LONG_WAIT_TIME = 5  # seconds
SHORT_WAIT_TIME = 5

def _get_secret(name: str, default: str = "") -> str:
    """Lit <NAME>_FILE (docker secret) en priorité, sinon <NAME>."""
    path = os.getenv(f"{name}_FILE")
    if path and os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return os.getenv(name, default)


DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "woody-app")
DB_PASS = _get_secret("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "woody")
DB_PORT = int(os.getenv("DB_PORT", "3306"))

def my_connect():

    try:
        mydb = connect(host=DB_HOST, user=DB_USER, password=DB_PASS,
                       database=DB_NAME, port=DB_PORT)
        mycursor = mydb.cursor()
    except Error as e:
        print(e)
        return None, None
    return mydb, mycursor


def get_last_product():
    mydb, mycursor = my_connect()

    mycursor.execute("LOCK TABLES product READ;")

    mycursor.execute("SELECT name, sleep(15) FROM product ORDER BY id DESC LIMIT 1;")

    last_product = mycursor.fetchone()

    mycursor.execute("select count(*) from product;")
    product_count = mycursor.fetchone()

    # sleep(SHORT_WAIT_TIME)

    mycursor.execute("UNLOCK TABLES;")
    mycursor.close()
    mydb.close()

    if last_product is None or product_count is None:
        return "No product found"

    return f'{product_count[0]} products (last={last_product[0]})'


def make_some_heavy_computation(param=""):
    sleep(LONG_WAIT_TIME)
    return f"Woody -{param}- Woody"


def make_heavy_validation(order):
    make_some_heavy_computation()
    return "Success"


def add_product(product):
    mydb, mycursor = my_connect()
    mycursor.execute(
        "INSERT INTO woody.product (name) VALUES (%s);",
        (product,),
    )
    mydb.commit()
    mycursor.close()
    mydb.close()


def launch_server(app, host='0.0.0.0', port=5000):
    run_simple(host, port, app, use_reloader=True, threaded=False)


def save_order(order_id, status, product):
    mydb, mycursor = my_connect()
    mycursor.execute(
        "INSERT INTO woody.order (order_id, status, product) VALUES (%s, %s, %s);",
        (order_id, status, product),
    )
    mydb.commit()

    mycursor.close()
    mydb.close()


def get_order(order_id):
    mydb, mycursor = my_connect()
    mycursor.execute(
        "SELECT status FROM woody.order WHERE order_id=%s;",
        (order_id,),
    )

    order_status = mycursor.fetchone()

    mycursor.close()
    mydb.close()
    return order_status
