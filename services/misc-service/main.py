from datetime import datetime
from time import sleep

from flask import Flask, request, jsonify

from redis_wrapper import cache_result

app = Flask(__name__)


@app.get("/api/misc/heavy")
@cache_result(ttl=30)
def heavy():
    name = request.args.get("name", "world")
    sleep(1.5)   # simule une charge CPU / latence
    return f"{datetime.now()}: hello {name}"


@app.get("/api/misc/time")
def get_time():
    return f"misc: {datetime.now()}"


@app.get("/healthz")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
