import os, json, time, pika

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "woody")
RABBIT_PASS = os.getenv("RABBIT_PASS", "woodypass")
QUEUE_NAME  = os.getenv("QUEUE_NAME", "order_processing")

def process(order_id, product):
    # Simule un traitement lourd
    time.sleep(1.5)
    print(f"[worker] processed order={order_id} product={product}")

def main():
    creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    conn  = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, credentials=creds))
    ch    = conn.channel()
    ch.queue_declare(queue=QUEUE_NAME, durable=True)
    ch.basic_qos(prefetch_count=10)

    def callback(ch_, method, props, body):
        try:
            message = json.loads(body)
            process(message.get("order_id"), message.get("product"))
            ch_.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("Error:", e)
            ch_.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    ch.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print("[worker] waiting messages…")
    ch.start_consuming()

if __name__ == "__main__":
    main()
