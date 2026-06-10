# 🚀 WebSocket vs REST - Real-Time Chat Demo

## 📌 Overview

This project demonstrates the difference between:

- REST (Request-Response)
- Polling
- Server-Sent Events (SSE)
- WebSockets (Real-time communication)

We also build a simple chat application using WebSockets.

---

## 🧠 Concepts Covered

### ✅ REST
- Stateless
- Request → Response → Connection closed

### ✅ Polling
- Client repeatedly asks server for updates

### ✅ Server-Sent Events (SSE)
- One-way communication (Server → Client)

### ✅ WebSocket
- Persistent connection
- Full duplex communication (Client ⇄ Server)

---

## 🏗️ Architecture

### REST
Client → Server → Response → Close

### Polling
Client → Request → Server (Repeated)

### SSE
Server ─────▶ Client

### WebSocket
Client ⇄ Server (Continuous Connection)

---

## ⚙️ Tech Stack

- Python
- WebSockets library

---

## 📂 Project Structure

