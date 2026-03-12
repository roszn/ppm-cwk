function react(id, type) {
    fetch(`/${type}/${id}`, {
        method: 'POST'
    })
    .then(res => res.json())
    .then(data => {
        const span = document.getElementById(`${type}-${id}`);
        if (span) {
            span.innerText = data.new_count;
        }
    })
    .catch(err => console.error('Error:', err));
}