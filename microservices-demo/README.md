# Microservices Demo — User, Product & Order Services

A hands-on microservices project with three independently running Flask services that communicate with each other over REST. Built to demonstrate real-world service decomposition, inter-service communication, and fault isolation.

---

## Architecture

```
                        ┌─────────────────┐
                        │   Order Service  │
                        │   (Port 8003)    │
                        └────────┬────────┘
                                 │ REST calls
               ┌─────────────────┴──────────────────┐
               ↓                                    ↓
   ┌───────────────────┐               ┌───────────────────┐
   │   User Service    │               │  Product Service  │
   │   (Port 8001)     │               │   (Port 8002)     │
   └───────────────────┘               └───────────────────┘
```

When an order is placed, the **Order Service** does the following automatically:

1. Calls **User Service** → validates if the user exists and is active
2. Calls **Product Service** → checks if the product is in stock
3. Reserves the stock
4. Confirms the order

---

## Project Structure

```
microservices-demo/
├── user-service/
│   ├── app.py                  ← Manages user data and validation
│   ├── requirements.txt
│   └── Dockerfile
├── product-service/
│   ├── app.py                  ← Manages product catalog and stock
│   ├── requirements.txt
│   └── Dockerfile
├── order-service/
│   ├── app.py                  ← Orchestrates user + product, creates orders
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml          ← Runs all 3 services together
├── demo.py                     ← Automated test script for all scenarios
└── README.md
```

---

## Services at a Glance

| Service | Port | Responsibility |
|---------|------|----------------|
| User Service | 8001 | Store and validate user accounts |
| Product Service | 8002 | Manage product catalog and stock levels |
| Order Service | 8003 | Validate user + stock, then create order |

---

## Pre-loaded Demo Data

### Users

| ID | Name | Status |
|----|------|--------|
| 1 | Vijay Sharma | ✅ Active |
| 2 | Bhumika Gupta | ✅ Active |
| 3 | Priya Singh | ❌ Inactive |

### Products

| ID | Name | Price | Stock |
|----|------|-------|-------|
| 101 | iPhone 15 | ₹79,999 | 50 |
| 102 | Samsung S24 | ₹69,999 | 0 (Out of stock) |
| 103 | OnePlus 12 | ₹49,999 | 25 |

---

## Option A — Run with Docker (Recommended)

> Docker handles everything — no manual terminal juggling required.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Steps

**Step 1 — Open a terminal in the project folder**

```bash
cd microservices-demo
```

**Step 2 — Build and start all services**

```bash
docker-compose up --build
```

You will see all three services start one by one. Order Service waits for User and Product services to be healthy before it starts — this is automatic.

**Step 3 — Confirm all services are running**

Open your browser and visit these URLs:

- [http://localhost:8001/health](http://localhost:8001/health) → User Service
- [http://localhost:8002/health](http://localhost:8002/health) → Product Service
- [http://localhost:8003/health](http://localhost:8003/health) → Order Service

Each should return:
```json
{"service": "...", "status": "healthy"}
```

**Step 4 — Open a new terminal and run the demo**

```bash
python demo.py
```

**Step 5 — Stop all services**

```bash
docker-compose down
```

---

## Option B — Run Without Docker (3 Terminals)

> Run each service manually in a separate terminal window.

### Prerequisites

- Python 3.8 or above installed

### Important — Update URLs in Order Service

Before running, open `order-service/app.py` and change these two lines:

```python
# Change this:
USER_SERVICE = "http://user-service:8001"
PRODUCT_SERVICE = "http://product-service:8002"

# To this:
USER_SERVICE = "http://localhost:8001"
PRODUCT_SERVICE = "http://localhost:8002"
```

> This is only needed for local runs. Docker uses service names instead of localhost.

---

### Terminal 1 — Start User Service

```bash
cd user-service
pip install -r requirements.txt
python app.py
```

Expected output:
```
User Service running on port 8001
```

---

### Terminal 2 — Start Product Service

```bash
cd product-service
pip install -r requirements.txt
python app.py
```

Expected output:
```
Product Service running on port 8002
```

---

### Terminal 3 — Start Order Service

```bash
cd order-service
pip install -r requirements.txt
python app.py
```

Expected output:
```
Order Service running on port 8003
```

---

### Terminal 4 — Run the Demo

```bash
cd microservices-demo
pip install requests
python demo.py
```

---

## Demo Scenarios

The `demo.py` script runs 5 scenarios automatically. Here is what each one tests:

---

### Scenario 1 — Valid Order ✅

**What happens:** User 1 (Vijay) orders iPhone 15 (Product 101)

**Expected flow:**
```
Order Service → User Service  : "Is User 1 valid?"     → Yes ✅
Order Service → Product Service : "Is Product 101 in stock?" → Yes (50 units) ✅
Order Service → Product Service : "Reserve 1 unit"     → Done ✅
Order Service : Order CONFIRMED ✅
```

**Expected response:**
```json
{
  "success": true,
  "order": {
    "order_id": "A3F2B1C9",
    "user_id": 1,
    "product_id": 101,
    "quantity": 1,
    "status": "CONFIRMED"
  },
  "message": "Order placed successfully"
}
```

---

### Scenario 2 — Inactive User ❌

**What happens:** User 3 (Priya — inactive) tries to place an order

**Expected flow:**
```
Order Service → User Service : "Is User 3 valid?" → No, user is inactive ❌
Order Service : Order REJECTED at user validation step
(Product Service is never contacted)
```

**Expected response:**
```json
{
  "success": false,
  "step_failed": "user_validation",
  "reason": "User is inactive"
}
```

---

### Scenario 3 — Out of Stock ❌

**What happens:** User 1 (Vijay) tries to order Samsung S24 (Product 102 — stock 0)

**Expected flow:**
```
Order Service → User Service  : "Is User 1 valid?"     → Yes ✅
Order Service → Product Service : "Is Product 102 in stock?" → No, out of stock ❌
Order Service : Order REJECTED at stock check step
```

**Expected response:**
```json
{
  "success": false,
  "step_failed": "stock_check",
  "reason": "Out of stock"
}
```

---

### Scenario 4 — User Does Not Exist ❌

**What happens:** User 999 (does not exist) tries to place an order

**Expected flow:**
```
Order Service → User Service : "Is User 999 valid?" → User not found ❌
Order Service : Order REJECTED immediately
```

**Expected response:**
```json
{
  "success": false,
  "step_failed": "user_validation",
  "reason": "User not found"
}
```

---

### Scenario 5 — Health Check ✅

**What happens:** Verifies all three services are up and running

**Expected response from each service:**
```json
{"service": "user-service",    "status": "healthy"}
{"service": "product-service", "status": "healthy"}
{"service": "order-service",   "status": "healthy"}
```

---

## API Reference

### User Service — Port 8001

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check if service is running |
| GET | `/users/{id}` | Get user details by ID |
| GET | `/users/{id}/validate` | Check if user is valid and active |

---

### Product Service — Port 8002

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check if service is running |
| GET | `/products/{id}` | Get product details by ID |
| GET | `/products/{id}/check-stock` | Check if product is in stock |
| POST | `/products/{id}/reserve` | Reserve 1 unit of the product |

---

### Order Service — Port 8003

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check if service is running |
| POST | `/orders` | Place a new order |
| GET | `/orders/{order_id}` | Get order details by order ID |

**POST `/orders` — Request Body:**
```json
{
  "user_id": 1,
  "product_id": 101,
  "quantity": 1
}
```

---

## Troubleshooting

**Services not starting?**
- Make sure no other application is using ports 8001, 8002, or 8003
- Run `pip install -r requirements.txt` inside each service folder before starting

**Order Service cannot reach User or Product Service?**
- If running without Docker, make sure you have updated the URLs in `order-service/app.py` to use `localhost` instead of service names (see Option B setup above)
- Make sure User Service and Product Service are running before starting Order Service

**`demo.py` shows connection errors?**
- All three services must be running before executing `demo.py`
- Check each service's health URL in the browser first

**Docker build fails?**
- Make sure Docker Desktop is open and running
- Try `docker-compose down` first, then `docker-compose up --build` again

---

## Key Concepts Demonstrated

| Concept | Where it appears |
|---------|-----------------|
| Service decomposition | Three separate services, each with one responsibility |
| REST communication | Order Service calls User and Product Service via HTTP |
| Fault isolation | One service failing does not crash the others |
| Health checks | `/health` endpoint on every service |
| Independent deployment | Each service has its own `Dockerfile` and `requirements.txt` |
| Docker networking | Services communicate by name inside Docker network |
| Graceful failure | Order is rejected at the exact step that fails, with a clear reason |
