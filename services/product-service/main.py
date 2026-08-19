import os
from flask import Flask, jsonify
import pymysql

from redis_wrapper import cache_result


def get_secret(name: str, default: str = "") -> str:
    path = os.getenv(f"{name}_FILE")
    if path and os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return os.getenv(name, default)


DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "woody-app")
DB_PASS = get_secret("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "woodytoys")

app = Flask(__name__)


@app.get("/api/products/last")
@cache_result(ttl=15)
def last_product():
    conn = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS,
        database=DB_NAME, connect_timeout=5,
    )
    try:
        with conn.cursor() as cur:
            # Requete parametree : pas de concatenation de chaine.
            cur.execute(
                "SELECT id, product_name, product_price "
                "FROM products ORDER BY id DESC LIMIT 1"
            )
            row = cur.fetchone()
    finally:
        conn.close()

    if not row:
        return "no products"
    return f"{row[0]} | {row[1]} | {row[2]}"


@app.get("/healthz")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
