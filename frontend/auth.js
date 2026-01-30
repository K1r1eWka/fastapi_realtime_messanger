async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    console.log(`Logging in with username: ${username} and password: ${password}`);

    const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    console.log(data);
    console.log(data["detail"]);
    document.getElementById("result").textContent = data["detail"];

    if (res.ok){
        window.location.href = "http://127.0.0.1:5500/frontend/index.html";
    }
}