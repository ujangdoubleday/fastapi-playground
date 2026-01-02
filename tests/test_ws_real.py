import asyncio
import websockets

async def hello():
    uri = "ws://127.0.0.1:8000/api/v4/ws"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send("Hello Server!")
            response = await websocket.recv()
            print(f"Received: {response}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(hello())
