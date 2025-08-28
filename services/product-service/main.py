from flask import Flask, jsonify
import os, pymysql

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "mypass")
DB_NAME = os.getenv("DB_NAME", "woodytoys")

app = Flask(__name__)

@app.get("/api/products/last")
def last_product():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    with conn.cursor() as cur:
        cur.execute("SELECT id, product_name, product_price FROM products ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
    conn.close()
    if not row: 
        return jsonify({"message":"no products"}), 404
    return jsonify({"id": row[0], "name": row[1], "price": row[2]})

@app.get("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
