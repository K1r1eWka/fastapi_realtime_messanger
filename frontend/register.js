        // Minimal client-side validation and password toggle
        const form = document.getElementById('registerForm');
        const username = document.getElementById('username');
        const email = document.getElementById('email');
        const password = document.getElementById('password');

        const usernameError = document.getElementById('usernameError');
        const emailError = document.getElementById('emailError');
        const passwordError = document.getElementById('passwordError');

        document.getElementById('showPwd').addEventListener('change', (e) => {
            password.type = e.target.checked ? 'text' : 'password';
        });

        form.addEventListener('submit', async (ev) => {
            ev.preventDefault();

            // clear errors
            usernameError.textContent = '';
            emailError.textContent = '';
            passwordError.textContent = '';

            let valid = true;

            if (username.value.trim().length < 3) {
                usernameError.textContent = 'Please enter a username (min 3 characters).';
                valid = false;
            }

            if (!email.checkValidity()) {
                emailError.textContent = 'Please enter a valid email address.';
                valid = false;
            }

            if (password.value.length < 8) {
                passwordError.textContent = 'Password must be at least 8 characters.';
                valid = false;
            }

            if (!valid) return;

            const res = await fetch('http://127.0.0.1:8000/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: username.value.trim(),
                    email: email.value.trim(),
                    password: password.value
                })
            });

            if (!res.ok) {
                const errorData = await res.json();
                console.log(errorData);
                document.getElementById('registrationMessage').textContent = errorData.detail || 'Registration failed.';
                return;
            }

            const data = await res.json();
            console.log('Registration successful:', data);
            window.location.href = "http://127.0.0.1:5500/frontend/login.html";
  

            console.log('Registration data looks good — submit to server.');
            alert('Registration data looks good — submit to server.');
            form.reset();
        });