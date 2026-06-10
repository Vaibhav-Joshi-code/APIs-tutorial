# 🚀 REST API from Scratch (FastAPI)

## 📌 Overview

This project demonstrates how a REST API works internally by building it from scratch using FastAPI.

It focuses on real backend concepts such as:
- State management
- HTTP methods
- API design
- Stateless architecture

---

## 🧠 What is REST?

REST stands for Representational State Transfer.

It means:
- System state is stored on server
- Client requests representation of that state
- Data is exchanged in structured format (JSON)

---

## ⚙️ Tech Stack

- Python
- FastAPI
- Uvicorn

---

## 📦 Endpoints

### Create User
POST /users

### Get Users
GET /users

### Get User
GET /users/{id}

### Update User
PUT /users/{id}

### Delete User
DELETE /users/{id}

---

## ▶️ Run Project

```bash
pip install fastapi uvicorn
uvicorn main:app --reload