// Dashboard functionality
function logout() {
    fetch('/logout/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
    });
}

function refreshProfile() {
    location.reload();
}

function viewUsers() {
    // This would typically redirect to a user management page
    alert('User management feature coming soon!');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}