var base_url = window.location.origin;
function get_cookie(name) {
    let cookie_value = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookie_value;
}
const csrftoken = get_cookie('csrftoken')
const sign_up_btn = document.querySelector('.sign_up_btn');
async function sign_up() {
    const username = document.getElementById('new_username').value;
    const password = document.getElementById('new_password').value;
    const nickname = document.getElementById('new_nickname').value;
    try {
        const result = await fetch(base_url + '/user/user_control', {
            method: 'POST',
            headers: {
                'Aceept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                "username": username,
                "password": password,
                "nickname": nickname
            })
        })
        if (result.ok) {
            location.replace('/user/sign_in/')
        }
    }
    catch (err) {
        console.log(err)
    }
}