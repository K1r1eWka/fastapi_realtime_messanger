from fastapi import WebSocket


class ActiveEventManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    # if user will decide delete its account
    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    # each user(websocket) in connections list will receive message
    async def breodcast(self, message: dict):
        for ws in self.active_connections:
            await ws.send_json(message)