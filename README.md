# FastAPI Realtime Messenger

Real-time chat backend built with **FastAPI**, **WebSockets**, **JWT authentication**, and **PostgreSQL**.

The project is a backend for a messenger with support for:
- user authorization
- chat rooms
- real-time messaging via WebSocket
- storing messages in a database
- loading message history when entering chat

---

## Features

- 🔐 JWT authentication (HTTP + WebSocket)
- 🍪 Token stored in HttpOnly cookies
- ⚡ Real-time messaging via WebSocket
- 🏠 Chat rooms (group chats)
- 💬 Message persistence (PostgreSQL)
- 🕓 Load last messages when joining a room
- 👤 Username shown for each message
- 🔒 Protected API endpoints

---

## Tech Stack

- **Backend**: FastAPI
- **Realtime**: WebSocket
- **Auth**: JWT (PyJWT)
- **Database**: PostgreSQL
- **ORM**: SQLModel (SQLAlchemy)
- **Frontend**: HTML / CSS / JavaScript (vanilla)

---

## Project Structure
```text
backend/
├── auth/              # JWT logic & dependencies
├── models/            # SQLModel database models
├── routers/           # HTTP & WebSocket routers
├── core/              # Config & settings
├── db/                # Database connection
├── main.py            # FastAPI entry point

frontend/
├── login.html
├── register.html
├── chat.html
├── script.js.         # For index.html
├── auth.js
├── register.js
├── styles.css
```

---

## Project Structure

    1.	User registers via HTTP (POST /register)
    2.	User logs in via HTTP (POST /login)
    3.	Server creates JWT and stores it in HttpOnly    cookie
    4.	Browser automatically sends cookie: to protected HTTP endpoints to WebSocket connection
    5.	Server validates token and links:

## Chat Flow

	1. User selects a chat room
	2. Frontend:
	    - fetches last messages via HTTP
	    - opens WebSocket connection
	3. Messages are:
	    - broadcasted to room participants
	    - saved to database
	4. New users see last messages on join

## Future Improvements

	-	Private 1-to-1 chats
	-	User invitations
	-	Message read status
    -   Real time video and audio calls
	-	Typing indicators
	-	Pagination for chat history
	-	Docker & docker-compose

## Built by K1r1eWka
Learning-focused project to deeply understand:
    -   WebSocket architecture
    -   Authentication & authorization
    -   Backend + frontend interaction
    -   Real-time systems
