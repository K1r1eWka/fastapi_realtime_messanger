document.addEventListener("DOMContentLoaded", loadUsers);

async function loadUsers() {
    try {
        const response = await fetch("http://127.0.0.1:8000/all_users", {
            credentials: "include" 
        });

        if (!response.ok) {
            console.error("Failed to load users");
            return;
        }

        const users = await response.json();
        renderUsers(users);
    } catch (err) {
        console.error("Error loading users:", err);
    }
}

function renderUsers(users) {
    const list = document.getElementById("usersList");
    list.innerHTML = "";

    users.forEach(user => {
        const li = document.createElement("div");
        li.classList.add("user")
        li.textContent = user.username;

        // feature for future 
        // li.onclick = () => {
        //     console.log("Open chat with user:", user.id);
        // };

        list.appendChild(li);
    });
}


let ws = null;
let currentRoom = null;

async function connectToRoom(room) {
    // если уже подключены — закрываем старое соединение
    if (ws) {
        ws.close();
    }

    currentRoom = room;

    document.getElementById("messages").innerHTML = "";
    document.getElementById("status").textContent = `Connecting to ${room}...`;

    const response = await fetch(`http://127.0.0.1:8000/ws/${room}/messages`, {
        credentials: "include"
    })
    const messages = await response.json()
    messages.forEach(addMessage)


    ws = new WebSocket(`ws://127.0.0.1:8000/ws/${room}`);

    ws.onopen = () => {
        document.getElementById("status").textContent =
            `Connected to ${room}`;
    };

    ws.onmessage = (event) => {
        addMessage(event.data);
    };

    ws.onclose = () => {
        document.getElementById("status").textContent =
            `Disconnected`;
    };

    ws.onerror = (err) => {
        console.error("WebSocket error", err);
    };
}

function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value.trim();

    if (!message || !ws) return;

    ws.send(message);
    input.value = "";
}

function addMessage(text) {
    const messages = document.getElementById("messages");
    const div = document.createElement("div");
    div.classList.add("your_message");
    div.textContent = text;
    messages.appendChild(div);
}