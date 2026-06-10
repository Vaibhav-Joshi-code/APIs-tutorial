# ⚡ API Comparison — REST vs GraphQL vs gRPC

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=flat-square&logo=graphql)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> A hands-on project demonstrating the **real difference** between REST, GraphQL, and gRPC — with live servers, response comparisons, and side-by-side output.  
> Built as part of the **API Design Series** on YouTube.

---

## 📑 Table of Contents

- [What This Project Proves](#-what-this-project-proves)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Running the Servers](#-running-the-servers)
- [REST API — Endpoints & Examples](#-rest-api--endpoints--examples)
- [GraphQL API — Queries & Examples](#-graphql-api--queries--examples)
- [Side-by-Side Comparison Demo](#-side-by-side-comparison-demo)
- [Key Concepts Explained](#-key-concepts-explained)
- [When to Use What](#-when-to-use-what)
- [Author](#-author)

---

## 🎯 What This Project Proves

Same data. Same database. Two completely different API approaches.

| Problem | REST | GraphQL |
|---------|------|---------|
| Get user name + their post titles | ❌ 2 separate requests | ✅ 1 single query |
| Extra unwanted data in response | ❌ Yes (over-fetching) | ✅ No — you ask, you get |
| Flexibility for client | ❌ Server decides response shape | ✅ Client decides response shape |
| Single endpoint | ❌ Multiple endpoints | ✅ Always `/graphql` |

---

## 🛠 Tech Stack

| Tool | Used For |
|------|---------|
| **Python 3.10+** | Primary language |
| **Flask** | REST server (port 5000) |
| **Flask-GraphQL + Graphene** | GraphQL server (port 5001) |
| **Requests** | Demo script HTTP calls |
| **JSON** | Response formatting |

---

## 📁 Project Structure

```
api-comparison/
│
├── rest_server.py          # REST API server — runs on port 5000
├── graphql_app.py       # GraphQL API server — runs on port 5001
├── demo_comparison.py      # Script that hits both servers and shows response diff
├── requirements.txt        # All dependencies
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Vaibhav-Joshi-code/APIs-tutorial.git
cd api-comparison
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` contents:**
```
flask
flask-graphql
graphene
requests
```

---

## ▶️ Running the Servers

You need **3 terminals** open simultaneously.

### Terminal 1 — Start REST Server

```bash
python rest_server.py
```

```
* Running on http://127.0.0.1:5000
```

### Terminal 2 — Start GraphQL Server

```bash
python graphql_app.py
```

```
* Running on http://127.0.0.1:5001
```

### Terminal 3 — Run the Comparison Demo

```bash
python demo_comparison.py
```

---

## 📡 REST API — Endpoints & Examples

**Base URL:** `http://127.0.0.1:5000`

### Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| `GET` | `/users` | Get all users | `200 OK` |
| `GET` | `/users/{user_id}` | Get a single user by ID | `200 OK` / `404` |
| `GET` | `/users/{user_id}/posts` | Get all posts by a user | `200 OK` |

---

#### `GET /users` — Get All Users

**Request:**
```bash
curl -X GET http://127.0.0.1:5000/users
```

**Response — `200 OK`:**
```json
[
  {
    "id": 1,
    "name": "Vijay",
    "email": "vijay@example.com",
    "age": 22,
    "city": "Jaipur"
  },
  {
    "id": 2,
    "name": "Bhumika",
    "email": "bhumika@example.com",
    "age": 21,
    "city": "Delhi"
  }
]
```

> ⚠️ **Notice:** Even if you only need the `name`, you still get `email`, `age`, and `city`. This is **over-fetching**.

---

#### `GET /users/{user_id}` — Get Single User

**Request:**
```bash
curl -X GET http://127.0.0.1:5000/users/1
```

**Response — `200 OK`:**
```json
{
  "id": 1,
  "name": "Vijay",
  "email": "vijay@example.com",
  "age": 22,
  "city": "Jaipur"
}
```

**Response — `404 Not Found`:**
```json
{
  "error": "Not found"
}
```

---

#### `GET /users/{user_id}/posts` — Get User's Posts

**Request:**
```bash
curl -X GET http://127.0.0.1:5000/users/1/posts
```

**Response — `200 OK`:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "REST API Basics",
    "body": "REST is great for CRUD"
  },
  {
    "id": 2,
    "user_id": 1,
    "title": "Docker Intro",
    "body": "Docker simplifies deployment"
  }
]
```

> ⚠️ **Notice:** To get user name + post titles together, you need **2 separate requests** — one to `/users/1` and another to `/users/1/posts`. This is **under-fetching / N+1 problem**.

---

## 🔷 GraphQL API — Queries & Examples

**Base URL:** `http://127.0.0.1:5001/graphql`

> GraphQL always uses a **single endpoint** and **POST method**. The query goes inside the request body.

### GraphiQL Interactive Explorer

Open in your browser:
```
http://127.0.0.1:5001/graphql
```
This gives you a live playground to write and test GraphQL queries.

---

#### Query 1 — Get User Name + Post Titles (Single Request)

**Query:**
```graphql
{
  user(id: 1) {
    name
    posts {
      title
    }
  }
}
```

**Request via curl:**
```bash
curl -X POST http://127.0.0.1:5001/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: 1) { name posts { title } } }"}'
```

**Response — `200 OK`:**
```json
{
  "data": {
    "user": {
      "name": "Vijay",
      "posts": [
        { "title": "REST API Basics" },
        { "title": "Docker Intro" }
      ]
    }
  }
}
```

> ✅ **Notice:** Only `name` and `title` came back. No `email`, no `age`, no `body`. Exactly what was asked — nothing more, nothing less.

---

#### Query 2 — Get Only User Email

**Query:**
```graphql
{
  user(id: 1) {
    email
  }
}
```

**Response:**
```json
{
  "data": {
    "user": {
      "email": "vijay@example.com"
    }
  }
}
```

---

#### Query 3 — Get All Users (Only Names)

**Query:**
```graphql
{
  users {
    name
  }
}
```

**Response:**
```json
{
  "data": {
    "users": [
      { "name": "Vijay" },
      { "name": "Bhumika" }
    ]
  }
}
```

---

## 🔬 Side-by-Side Comparison Demo

Run `demo_comparison.py` and you will see this output in the terminal:

```
============================================================
REST API — We want only the user's name, but extra data will also come
============================================================
REST Response (everything came — age, city too):
{
  "id": 1,
  "name": "Vijay",
  "email": "vijay@example.com",    <-- NOT needed
  "age": 22,                        <-- NOT needed
  "city": "Jaipur"                  <-- NOT needed
}

For posts, we had to make a separate request:
[
  { "id": 1, "user_id": 1, "title": "REST API Basics", "body": "..." },
  { "id": 2, "user_id": 1, "title": "Docker Intro",    "body": "..." }
]

============================================================
GraphQL — We asked only for name and post titles
============================================================
GraphQL Response (exactly what we asked for — nothing extra):
{
  "data": {
    "user": {
      "name": "Vijay",
      "posts": [
        { "title": "REST API Basics" },
        { "title": "Docker Intro" }
      ]
    }
  }
}

  REST   → 2 requests needed + extra unwanted data came
✅ GraphQL → 1 request + exactly what we asked for
```

---

## 💡 Key Concepts Explained

### Over-fetching
When the server sends **more data than the client needs**.  
Example: You need only a user's name, but REST gives you name + email + age + city.

### Under-fetching / N+1 Problem
When one request is **not enough** and you need to make additional requests to complete the data.  
Example: Need user + posts → two separate REST calls.

### Persistent Connection (WebSocket)
A long-lived connection where both client and server can send messages anytime.  
Used in real-time apps like chat, live scores, trading platforms.

### Protocol Buffers (gRPC)
Binary data format used by gRPC — much smaller and faster than JSON.  
Not human-readable but extremely efficient for internal service-to-service communication.

---

## 🗺 When to Use What

| Scenario | Best Choice | Reason |
|----------|------------|--------|
| Public API (Twitter, GitHub) | **REST** | Simple, widely understood, easy to cache |
| Mobile app with limited bandwidth | **GraphQL** | Fetch only what you need — saves data |
| Complex dashboard with nested data | **GraphQL** | Single query for all nested relationships |
| Microservices talking internally | **gRPC** | Binary format — ultra fast, strongly typed |
| Real-time chat / live scores | **WebSocket** | Persistent bidirectional connection |
| Simple CRUD application | **REST** | Standard, well-supported, easy to debug |

---


⭐ If this helped you understand the difference, drop a star and share with your batchmates!
