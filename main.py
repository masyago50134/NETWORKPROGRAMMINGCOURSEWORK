import requests
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

# Дані для Basic Auth
USERS = {
    "admin": "1234",
}

# Початкові дані для REST API (ЛБ3)
ITEMS = {
    1: {"name": "T-shirt", "price": 20, "color": "red"},
    2: {"name": "Jeans", "price": 50, "color": "blue"},
}

# Декоратор для перевірки аутентифікації
def check_auth(username, password):
    return USERS.get(username) == password

def requires_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    return wrapper

# --- Завдання з ЛБ2: Курси валют ---

@app.route("/")
def hello():
    return "Hello World! Coursework API is running."

@app.route("/currency", methods=["GET"])
def get_currency():
    # Отримуємо параметр дати (today або yesterday)
    param = request.args.get("date", "today")
    
    # Логіка для визначення дати для НБУ (формат YYYYMMDD)
    from datetime import datetime, timedelta
    if param == "yesterday":
        target_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    else:
        target_date = datetime.now().strftime("%Y%m%d")

    try:
        # Запит до реального API НБУ
        response = requests.get(f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={target_date}&json")
        data = response.json()
        
        if data:
            rate = data[0]['rate']
            return f"USD rate for {param}: {rate}"
        return "Currency data not found", 404
    except Exception as e:
        return f"Error fetching currency: {str(e)}", 500

# --- Завдання з ЛБ3: REST API для товарів ---

@app.route("/items", methods=["GET", "POST"])
@requires_auth
def items():
    if request.method == "GET":
        return jsonify(ITEMS)

    if request.method == "POST":
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        new_id = max(ITEMS.keys(), default=0) + 1
        ITEMS[new_id] = data
        return jsonify({"id": new_id, "item": data}), 201

@app.route("/items/<int:item_id>", methods=["GET", "PUT", "DELETE"])
@requires_auth
def item_by_id(item_id):
    if item_id not in ITEMS:
        return jsonify({"error": "Item not found"}), 404

    if request.method == "GET":
        return jsonify(ITEMS[item_id])

    if request.method == "PUT":
        data = request.json
        ITEMS[item_id].update(data)
        return jsonify(ITEMS[item_id])

    if request.method == "DELETE":
        del ITEMS[item_id]
        return jsonify({"message": "Deleted"}), 200

if __name__ == "__main__":
    # Запуск на порту 8000, як вказано в завданні
    app.run(host="0.0.0.0", port=8000)