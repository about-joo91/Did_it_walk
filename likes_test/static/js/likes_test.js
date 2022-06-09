function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }
        }
    }

    return cookieValue;
}


const csrftoken = getCookie('csrftoken')
const like_button = document.querySelector('.heart_btn')
async function like(post_id) {
    const result = await fetch('http://127.0.0.1:8000/likes_test/' + post_id + '/', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Aceept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (result.ok) {
        like_button.classList.contains("bi-heart-fill") ? like_button.classList.replace('bi-heart-fill', 'bi-heart') : like_button.classList.replace('bi-heart', 'bi-heart-fill')
    }
}