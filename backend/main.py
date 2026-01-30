from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import backend.routers.user as user
import backend.routers.web_socket as web_socket


app = FastAPI()
app.include_router(user.router)
app.include_router(web_socket.router)

# CORS middleware that allow send and take data between hosts(frontend and server(backend))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

