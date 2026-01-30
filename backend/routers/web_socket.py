from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime

from sqlmodel import select
from backend.core.config import security_settings
import jwt

from backend.db.database import SessionDep
from backend.models.message import Message
from backend.models.user import User


router = APIRouter(prefix="/ws")

# Manager which control WebSockets in all messanger system
class RoomConnectionManager:
    def __init__(self) -> None:
        self.rooms: dict[str, list[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
        self.rooms[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.rooms:
            if websocket in self.rooms[room_id]:
                self.rooms[room_id].remove(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def broadcast(self, room_id: str, message: str, sender: WebSocket):
        if room_id not in self.rooms:
            return
        for connection in self.rooms[room_id].copy():
            if connection == sender:
                continue
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(room_id, connection)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = RoomConnectionManager()


# endpoint that creates a websocket client and checks via cookie and jwt token which user is writing the message
@router.websocket("/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, session: SessionDep):
    await manager.connect(room_id, websocket)
    token = websocket.cookies.get("access_token")

    if not token:
        await websocket.close()
        return

    try:
        payload = jwt.decode(token, security_settings.JWT_SECRET, algorithms=[security_settings.JWT_ALGORITHM])
    except jwt.PyJWTError:
        await websocket.close()
        return

    user_id = payload["user_id"]
    username = payload["username"]

    await websocket.send_text(f"[{datetime.now().strftime('%H:%M:%S')}] Connected to room {room_id}")


    try:
        while True:
            data = await websocket.receive_text()
            created_at = datetime.now().strftime('%H:%M:%S')
            
            message = Message(
                chat_id=int(room_id),
                user_id=user_id,
                content=data,
            )
            session.add(message)
            session.commit()
            session.refresh(message)

            
            await manager.send_personal_message(
                f"[{created_at}] You: {data}",
                websocket
            )
            await manager.broadcast(
                room_id,
                f"[{created_at}][{username}]: {data}",
                websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        await manager.broadcast(
            room_id,
            f"[{datetime.now().strftime('%H:%M:%S')}][{username}] left the room",
            websocket
        )


# endpoint that take last 10 messages from data base and return a list of ready messages
@router.get("/{room_id}/messages")
def get_room_messages(room_id: str, session: SessionDep):
    # query data form bd, passing room_id -> get 10 last messages data 
    statement = select(Message).where(Message.chat_id == int(room_id)).order_by(Message.created_at.desc()).limit(10)
    result = session.exec(statement).all()
    
    # reverse list of rows and from each row creat message string and return new list with str messages
    message_objects = list(reversed(result))
    messages = []
    for message_obj in message_objects:
        statement = select(User).where(User.id == message_obj.user_id)
        user = session.exec(statement).one()
        message = f"[{message_obj.created_at.strftime("%H:%M")}] {user.username}: {message_obj.content}"
        messages.append(message)

    return messages