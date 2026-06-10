import asyncio
import websockets
import sys

async def receive_messages(websocket):
    """Task to constantly listen for incoming messages."""
    try:
        async for message in websocket:
            # Use \r to overwrite the current line so it doesn't mess up the "You: " prompt
            sys.stdout.write(f"\rOther: {message}\nYou: ")
            sys.stdout.flush()
    except websockets.exceptions.ConnectionClosed:
        print("\n❌ Disconnected from server.")

async def send_messages(websocket):
    """Task to handle user input and send messages."""
    while True:
        
        msg = await asyncio.to_thread(input, "")
        
        if msg.lower() in ['quit', 'exit']:
            break
            
        await websocket.send(msg)
        # Re-print "You: " after sending a message
        sys.stdout.write("You: ")
        sys.stdout.flush()

async def chat():
    uri = "ws://localhost:8765"
    print(f"🔄 Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected! Type a message and press Enter (or type 'quit' to exit).")
            sys.stdout.write("You: ")
            sys.stdout.flush()

            # Create concurrent tasks
            receive_task = asyncio.create_task(receive_messages(websocket))
            send_task = asyncio.create_task(send_messages(websocket))

            # Wait until either task finishes (e.g., user types 'quit' or server closes)
            done, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            # Cancel the remaining task
            for task in pending:
                task.cancel()

    except ConnectionRefusedError:
        print("❌ Connection failed. Is the server running?")

if __name__ == "__main__":
    asyncio.run(chat())