from flask import Flask, jsonify, request

app = Flask(__name__)

products = {
    101: {"id": 101, "name": "iPhone 15", "price": 79999, "stock": 50},
    102: {"id": 102, "name": "Samsung S24", "price": 69999, "stock": 0},
    103: {"id": 103, "name": "OnePlus 12", "price": 49999, "stock": 25},
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"service": "product-service", "status": "healthy"})

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

@app.route('/products/<int:product_id>/check-stock', methods=['GET'])
def check_stock(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({"available": False, "reason": "Product not found"}), 404
    if product["stock"] == 0:
        return jsonify({"available": False, "reason": "Out of stock"})
    return jsonify({"available": True, "stock": product["stock"]})

@app.route('/products/<int:product_id>/reserve', methods=['POST'])
def reserve_stock(product_id):
    product = products.get(product_id)
    if not product or product["stock"] == 0:
        return jsonify({"success": False, "reason": "Cannot reserve"}), 400
    products[product_id]["stock"] -= 1
    return jsonify({"success": True, "remaining_stock": product["stock"]})

if __name__ == '__main__':
    print("Product Service running on port 8002")
    app.run(host="0.0.0.0", port=8002, debug=True)
