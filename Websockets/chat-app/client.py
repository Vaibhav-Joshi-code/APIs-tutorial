import asyncio
import websockets

async def chat():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            msg = input("You: ")
            await websocket.send(msg)
            response = await websocket.recv()
            print("Other:", response)

asyncio.run(chat())