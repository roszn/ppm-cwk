// Registration form handling
document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData);

    fetch('/api/users/register/', {
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
            // Display errors
            let errorHtml = '';
            for (const [field, errors] of Object.entries(data)) {
                errorHtml += `<li>${field}: ${errors.join(', ')}</li>`;
            }
            document.querySelector('.alert-danger ul').innerHTML = errorHtml;
            document.querySelector('.alert-danger').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Registration failed');
    });
});