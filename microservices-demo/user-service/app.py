from flask import Flask, jsonify

app = Flask(__name__)

users = {
    1: {"id": 1, "name": "Vijay Sharma", "email": "vijay@example.com", "active": True},
    2: {"id": 2, "name": "Bhumika Gupta", "email": "bhumika@example.com", "active": True},
    3: {"id": 3, "name": "Priya Singh", "email": "priya@example.com", "active": False},
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"service": "user-service", "status": "healthy"})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/users/<int:user_id>/validate', methods=['GET'])
def validate_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"valid": False, "reason": "User not found"}), 404
    if not user["active"]:
        return jsonify({"valid": False, "reason": "User is inactive"}), 400
    return jsonify({"valid": True, "user": user})

if __name__ == '__main__':
    print("User Service running on port 8001")
    app.run(host="0.0.0.0", port=8001, debug=True)
