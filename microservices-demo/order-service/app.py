from flask import Flask, jsonify, request
import requests
import uuid
from datetime import datetime

app = Flask(__name__)

USER_SERVICE = "http://user-service:8001"
PRODUCT_SERVICE = "http://product-service:8002"

orders = {}

def validate_user(user_id):
    try:
        response = requests.get(f"{USER_SERVICE}/users/{user_id}/validate", timeout=5)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"valid": False, "reason": "User Service unavailable"}

def check_product_stock(product_id):
    try:
        response = requests.get(f"{PRODUCT_SERVICE}/products/{product_id}/check-stock", timeout=5)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"available": False, "reason": "Product Service unavailable"}

def reserve_product(product_id):
    try:
        response = requests.post(f"{PRODUCT_SERVICE}/products/{product_id}/reserve", timeout=5)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"success": False, "reason": "Product Service unavailable"}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"service": "order-service", "status": "healthy"})

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not user_id or not product_id:
        return jsonify({"error": "user_id and product_id required"}), 400

    print(f"[Order Service] Validating user {user_id}...")
    user_check = validate_user(user_id)
    if not user_check.get("valid"):
        return jsonify({"success": False, "step_failed": "user_validation", "reason": user_check.get("reason")}), 400

    print(f"[Order Service] Checking stock for product {product_id}...")
    stock_check = check_product_stock(product_id)
    if not stock_check.get("available"):
        return jsonify({"success": False, "step_failed": "stock_check", "reason": stock_check.get("reason")}), 400

    print(f"[Order Service] Reserving product {product_id}...")
    reservation = reserve_product(product_id)
    if not reservation.get("success"):
        return jsonify({"success": False, "step_failed": "reservation", "reason": reservation.get("reason")}), 400

    order_id = str(uuid.uuid4())[:8].upper()
    order = {
        "order_id": order_id,
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity,
        "status": "CONFIRMED",
        "created_at": datetime.now().isoformat()
    }
    orders[order_id] = order
    print(f"[Order Service] Order {order_id} created successfully!")
    return jsonify({"success": True, "order": order, "message": "Order placed successfully"}), 201

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order)

if __name__ == '__main__':
    print("Order Service running on port 8003")
    app.run(host="0.0.0.0", port=8003, debug=True)
