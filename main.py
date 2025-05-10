from flask import Flask, request
import requests, time, hmac, hashlib, json

app = Flask(__name__)

API_KEY = "INSERISCI_API_KEY"
API_SECRET = "INSERISCI_API_SECRET"
API_PASS = "INSERISCI_API_PASS"
BASE_URL = "https://api.bitget.com"

def sign_request(timestamp, method, path, body):
    message = f"{timestamp}{method}{path}{json.dumps(body)}"
    return hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.data.decode("utf-8")
    try:
        side, symbol, qty, leverage, tp, sl = data.strip().split("|")
    except:
        return "Invalid data format", 400

    timestamp = str(int(time.time() * 1000))
    path = "/api/mix/v1/order/placeOrder"
    body = {
        "symbol": symbol,
        "marginCoin": "USDT",
        "side": side.lower(),
        "orderType": "market",
        "size": qty,
        "leverage": leverage
    }

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": sign_request(timestamp, "POST", path, body),
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASS,
        "Content-Type": "application/json"
    }

    res = requests.post(BASE_URL + path, headers=headers, json=body)
    return res.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
