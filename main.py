from fastapi import FastAPI, WebSocket

app = FastAPI()

# Dictionary to store the connected WebSocket clients
connected_users = {}



@app.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: str, websocket: WebSocket):
    await websocket.accept()

    # Store the WebSocket connection in the dictionary
    connected_users[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            # Send the received data to the other user
            #await websocket.send_text(f"Message sent was : {data}")
            for user, user_ws in connected_users.items():
                if user != user_id:
                    await websocket.send_text(f"Message sent was : {data}")
                    await user_ws.send_text(f"Message Received : {data}")
    except:
        # If a user disconnects, remove them from the dictionary
        del connected_users[user_id]
        await websocket.close()

