import asyncio
import websockets

# Store all active connected clients
clients = set()

async def handler(websocket):
    # Register new client
    clients.add(websocket)
    print(f"✅ New client connected! Total clients: {len(clients)}")
    
    try:
        # Listen for messages from this client
        async for message in websocket:
            print(f"📩 Message received. Broadcasting to {len(clients) - 1} other client(s).")
            
            # Broadcast to everyone EXCEPT the sender
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ A connection was closed abruptly.")
    finally:
        # Unregister client on disconnect
        clients.remove(websocket)
        print(f"❌ Client disconnected. Total clients: {len(clients)}")

async def main():
    print("🚀 Starting WebSocket server on ws://localhost:8765...")
    # Start the server
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())