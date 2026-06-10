from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
users = [
    {"id": 1, "name": "Vijay", "email": "vijay@example.com", "age": 22, "city": "Jaipur"},
    {"id": 2, "name": "Bhumika", "email": "bhumika@example.com", "age": 21, "city": "Delhi"},
]

posts = [
    {"id": 1, "user_id": 1, "title": "REST API Basics", "body": "REST is great for CRUD"},
    {"id": 2, "user_id": 1, "title": "Docker Intro", "body": "Docker simplifies deployment"},
    {"id": 3, "user_id": 2, "title": "GraphQL Guide", "body": "GraphQL solves overfetching"},
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)  

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    return jsonify(user) if user else jsonify({"error": "Not found"}), 404

@app.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    user_posts = [p for p in posts if p['user_id'] == user_id]
    return jsonify(user_posts)  
if __name__ == '__main__':
    app.run(port=5000, debug=True)