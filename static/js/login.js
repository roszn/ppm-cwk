// Login form handling
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData);

    fetch('/api/users/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.tokens) {
            localStorage.setItem('access_token', data.tokens.access);
            localStorage.setItem('refresh_token', data.tokens.refresh);
            window.location.href = '/dashboard/';
        } else {
            alert(data.error || 'Login failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Login failed');
    });
});