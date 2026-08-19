import os
import json
import time

import pika


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


def process(order_id, product):
    time.sleep(1.5)   # simule un traitement lourd
    print(f"[worker] processed order={order_id} product={product}", flush=True)


def main():
    creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    # retry : le worker peut demarrer avant que RabbitMQ soit pret
    while True:
        try:
            conn = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBIT_HOST, credentials=creds)
            )
            break
        except pika.exceptions.AMQPConnectionError:
            print("[worker] rabbitmq indisponible, nouvel essai dans 5s", flush=True)
            time.sleep(5)

    ch = conn.channel()
    ch.queue_declare(queue=QUEUE_NAME, durable=True)
    ch.basic_qos(prefetch_count=10)

    def callback(ch_, method, props, body):
        try:
            message = json.loads(body)
            process(message.get("order_id"), message.get("product"))
            ch_.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("Error:", e, flush=True)
            # requeue=False : un message illisible reenfile en boucle sature la file
            ch_.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    ch.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print("[worker] waiting messages...", flush=True)
    ch.start_consuming()


if __name__ == "__main__":
    main()
