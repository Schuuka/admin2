from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.get("/api/misc/heavy")
def heavy():
    name = request.args.get("name","world")
    # Simuler une charge CPU/latence
    time.sleep(1.5)
    return jsonify({"hello": name, "status": "ok"})

@app.get("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
