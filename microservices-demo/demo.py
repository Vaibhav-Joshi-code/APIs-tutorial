import requests
import json

BASE_ORDER = "http://localhost:8003"
BASE_USER = "http://localhost:8001"
BASE_PRODUCT = "http://localhost:8002"

def print_section(title):
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)

def print_response(response):
    print(json.dumps(response.json(), indent=2))
    print(f"Status: {response.status_code}")

print_section("1. Health Check — All Services Running?")
for name, url in [("User", BASE_USER), ("Product", BASE_PRODUCT), ("Order", BASE_ORDER)]:
    r = requests.get(f"{url}/health")
    print(f"{name} Service: {r.json()['status']}")

print_section("2. Valid Order — User 1 orders iPhone (Product 101)")
response = requests.post(f"{BASE_ORDER}/orders", json={"user_id": 1, "product_id": 101, "quantity": 1})
print_response(response)

print_section("3. Inactive User — User 3 tries to order")
response = requests.post(f"{BASE_ORDER}/orders", json={"user_id": 3, "product_id": 101})
print_response(response)

print_section("4. Out of Stock — Anyone orders Samsung (Product 102)")
response = requests.post(f"{BASE_ORDER}/orders", json={"user_id": 1, "product_id": 102})
print_response(response)

print_section("5. Invalid User — User 999 does not exist")
response = requests.post(f"{BASE_ORDER}/orders", json={"user_id": 999, "product_id": 101})
print_response(response)
