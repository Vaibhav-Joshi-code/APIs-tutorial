# 🔀 Nginx Reverse Proxy + Load Balancer Demo





A hands-on demo to **visually understand** how Nginx works as a **Reverse Proxy** and **Load Balancer** — using two colorful backend servers and one Nginx config file.

***

## 🧠 What This Demo Proves

| Concept | How It's Demonstrated |
|---|---|
| **Reverse Proxy** | You only see `http://localhost` — port 8001/8002 is never exposed |
| **Load Balancing** | Browser alternates between 🟢 Green (Server A) and 🔵 Blue (Server B) |
| **Round Robin** | Nginx distributes requests A → B → A → B automatically |
| **Fault Tolerance** | Stop one container — Nginx routes all traffic to the surviving server |

***

## 🗂️ Project Structure

```
nginx-demo/
├── server-a/
│   └── index.html        ← 🟢 Green page — "I am Server A, Port 8001"
├── server-b/
│   └── index.html        ← 🔵 Blue page  — "I am Server B, Port 8002"
├── nginx.conf            ← Reverse Proxy + Load Balancer config (15 lines)
├── docker-compose.yml    ← Spins all 3 containers with one command
└── README.md
```

***

## ⚙️ How It Works — Architecture

```
You (Browser)
      │
      │  http://localhost (Port 80)
      ▼
┌─────────────────────┐
│      NGINX          │  ← Reverse Proxy — you never see 8001 or 8002
│  (nginx:alpine)     │  ← Load Balancer — Round Robin between A and B
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌─────────┐ ┌─────────┐
│Server A │ │Server B │
│Port 8001│ │Port 8002│
│ 🟢 Green│ │ 🔵 Blue │
└─────────┘ └─────────┘
```

**Key point:** Server A and Server B ports are **NOT exposed** to the host machine. The only way to reach them is through Nginx on port 80. This is the Reverse Proxy in action.

***

## 🔧 Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and **running**
- That's it — no Python, no Nginx installation needed locally

**Verify Docker is ready:**
```powershell
docker --version
docker-compose --version
```

Expected output:
```
Docker version 26.x.x
Docker Compose version v2.x.x
```

***

## 🚀 Run the Demo

### Step 1 — Start all containers

```powershell
docker-compose up --build
```

Wait until you see all three containers running:
```
Container server-a      Started ✅
Container server-b      Started ✅
Container nginx-proxy   Started ✅
```

### Step 2 — Open browser

```
http://localhost
```

You will see either the 🟢 **green page** (Server A) or 🔵 **blue page** (Server B).

### Step 3 — See Load Balancing in action

> ⚠️ **Important:** Use **Hard Refresh** to bypass browser cache.
>
> - **Windows/Linux:** `Ctrl + Shift + R`
> - **Mac:** `Cmd + Shift + R`

Each hard refresh alternates between servers:

```
Refresh 1 → 🟢 Server A (Port 8001)
Refresh 2 → 🔵 Server B (Port 8002)
Refresh 3 → 🟢 Server A (Port 8001)
Refresh 4 → 🔵 Server B (Port 8002)
```

### Step 4 — Confirm in Docker logs

Watch the terminal where `docker-compose up` is running:

```
server-a | "GET / HTTP/1.1" 200   ← Server A served this request
server-b | "GET / HTTP/1.1" 200   ← Server B served this request
server-a | "GET / HTTP/1.1" 200   ← Back to Server A
```

Nginx is alternating — **Round Robin Load Balancing confirmed.**

***

## 🔍 Verify in Browser DevTools

Open **Chrome DevTools → Network tab → Hard Refresh**

Click on the request → **Response Headers** tab:

```
X-Served-By: 172.18.0.2:8001    ← Server A handled this
```

Hard refresh again:

```
X-Served-By: 172.18.0.3:8002    ← Server B handled this
```

This `X-Served-By` header is added by our `nginx.conf` — it's direct proof of which backend server handled each request.

***

## 🧪 Fault Tolerance Test

**What happens when a server goes down?**

### Step 1 — Open Docker Desktop → Containers tab

### Step 2 — Stop `server-b` container (click the Stop ⏹ button)

### Step 3 — Hard refresh the browser multiple times

```
Refresh 1 → 🟢 Server A
Refresh 2 → 🟢 Server A   ← No crash! Nginx rerouted automatically
Refresh 3 → 🟢 Server A
```

No error. No downtime. Nginx detected Server B is down and sent all traffic to Server A.

### Step 4 — Restart `server-b` (click the Start ▶ button)

Round Robin automatically resumes — A, B, A, B...

> This is exactly what Netflix, YouTube, and Amazon do at scale — one server goes down, load balancer silently reroutes. Users notice nothing.

***

## 📄 nginx.conf — Explained

```nginx
events {
    worker_connections 1024;   # Max simultaneous connections
}

http {
    upstream backend_servers {
        server server-a:8001;  # Backend 1 — referenced by Docker service name
        server server-b:8002;  # Backend 2 — Round Robin by default
    }

    server {
        listen 80;             # Nginx listens on port 80

        location / {
            proxy_pass http://backend_servers;            # Forward to upstream
            proxy_set_header Host $host;                  # Pass original host
            proxy_set_header X-Real-IP $remote_addr;      # Pass real client IP
            add_header X-Served-By $upstream_addr always; # Show which backend responded
        }
    }
}
```

**Why `server-a:8001` instead of `localhost:8001`?**
Inside Docker, containers talk to each other using **service names** defined in `docker-compose.yml`, not localhost. Docker's internal DNS resolves `server-a` → correct container IP automatically.

***

## 🐳 docker-compose.yml — Explained

```yaml
services:
  server-a:
    image: python:3.11-slim       # No custom Dockerfile needed
    working_dir: /app
    volumes:
      - ./server-a:/app           # Mount server-a/index.html into container
    command: python -m http.server 8001   # Python's built-in HTTP server
    networks:
      - nginx-demo-network        # Private network — not accessible from outside

  server-b:
    image: python:3.11-slim
    working_dir: /app
    volumes:
      - ./server-b:/app
    command: python -m http.server 8002
    networks:
      - nginx-demo-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"                   # ONLY Nginx is exposed to the host
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf   # Our custom config
    depends_on:
      - server-a
      - server-b
    networks:
      - nginx-demo-network

networks:
  nginx-demo-network:
    driver: bridge                # Isolated bridge network for all 3 containers
```

**Notice:** `server-a` and `server-b` have **no `ports:` section** — they are unreachable from your browser directly. Only Nginx has `ports: "80:80"`. This enforces the Reverse Proxy pattern.

***

## 🛑 Stop the Demo

```powershell
docker-compose down
```

Output:
```
Container nginx-proxy   Stopped ✅
Container server-b      Stopped ✅
Container server-a      Stopped ✅
Network nginx-demo-network removed ✅
```

***

## 🐛 Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Page not changing on refresh | Browser cache | Use `Ctrl + Shift + R` (Hard Refresh) |
| `port 80 is already in use` | Another app using port 80 | Run `netstat -ano \| findstr :80` → kill that process, or change port to `"8080:80"` in compose |
| `docker-compose: command not found` | Older Docker version | Use `docker compose up --build` (no hyphen) |
| Both servers show same color | Hard refresh not used | Always use `Ctrl + Shift + R`, not `F5` |
| `server-a` or `server-b` not starting | Docker volume path issue | Ensure you are running the command from inside the `nginx-demo/` folder |

***

## 💡 Real World Connection

| This Demo | Production Scale |
|---|---|
| Server A + Server B | Hundreds of servers in AWS/GCP |
| `nginx.conf` upstream block | AWS Elastic Load Balancer / Nginx Plus |
| Docker bridge network | VPC private subnet |
| Hard refresh to switch servers | Millions of users, automatic distribution |
| Server B stopped → Server A takes over | Auto-healing, zero-downtime deployments |

***

## 📚 Concepts Covered

- **Reverse Proxy** — Client doesn't know which backend server exists
- **Load Balancing** — Traffic distributed across multiple servers
- **Round Robin Algorithm** — Default Nginx strategy, equal distribution
- **Fault Tolerance** — System continues when one server fails
- **Docker Networking** — Container-to-container communication via service names
- **HTTP 304 vs 200** — Why hard refresh matters for demo visibility