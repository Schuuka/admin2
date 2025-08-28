from flask import Flask, request, jsonify
import os, json, uuid, pika

app = Flask(__name__)

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "woody")
RABBIT_PASS = os.getenv("RABBIT_PASS", "woodypass")
QUEUE_NAME  = os.getenv("QUEUE_NAME", "order_processing")

def publish(msg: dict):
    creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    conn  = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, credentials=creds))
    ch    = conn.channel()
    ch.queue_declare(queue=QUEUE_NAME, durable=True)
    ch.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(msg),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    conn.close()

@app.get("/api/orders/do")
def make_order():
    product = request.args.get("order", "UnknownProduct")
    order_id = str(uuid.uuid4())
    publish({"order_id": order_id, "product": product})
    return jsonify({"queued": True, "order_id": order_id})

@app.get("/api/orders/status")
def status():
    return jsonify({"orders": "ok"})

@app.get("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)

