import os
import json
import re
import uuid

from flask import Flask, request, jsonify
import pika

app = Flask(__name__)


def get_secret(name: str, default: str = "") -> str:
    path = os.getenv(f"{name}_FILE")
    if path and os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return os.getenv(name, default)


RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "woody")
RABBIT_PASS = get_secret("RABBIT_PASS")
QUEUE_NAME = os.getenv("QUEUE_NAME", "order_processing")

PRODUCT_RE = re.compile(r"^[\w \-'À-ÿ]{1,100}$", re.UNICODE)


def publish(msg: dict):
    creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST, credentials=creds)
    )
    try:
        ch = conn.channel()
        ch.queue_declare(queue=QUEUE_NAME, durable=True)
        ch.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(msg),
            properties=pika.BasicProperties(delivery_mode=2),
        )
    finally:
        conn.close()


@app.post("/api/orders/do")
def make_order():
    payload = request.get_json(silent=True) or {}
    product = payload.get("order") or request.form.get("order")

    if not product or not PRODUCT_RE.match(str(product)):
        return jsonify({"error": "invalid or missing 'order'"}), 400

    order_id = str(uuid.uuid4())
    publish({"order_id": order_id, "product": str(product)})
    return jsonify({"queued": True, "order_id": order_id}), 202


@app.get("/api/orders/status")
def status():
    return jsonify({"orders": "ok"})


@app.get("/healthz")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
