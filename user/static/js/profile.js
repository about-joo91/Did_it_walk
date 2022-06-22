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
const edit_btn = document.querySelector('.edit_btn');
const mini_modal_wrapper = document.querySelector('.mini_modal_wrapper')
edit_btn.addEventListener('click', function () {
    mini_modal_wrapper.style.display = 'block'
})

mini_modal_wrapper.addEventListener('click', function (e) {
    if (e.target.classList.contains('mini_modal_wrapper')) {
        mini_modal_wrapper.style.display = 'none';
    }
})

const preview_profile_input = document.querySelector('.preview_profile_input');
const preview_profile = document.querySelector('.preview_profile');
preview_profile_input.addEventListener('change', function () {
    let image = this.files[0]
    const reader = new FileReader();
    reader.onload = () => {
        preview_profile.src = reader.result
    }
    reader.readAsDataURL(image)
})

const confirm_btn = document.querySelector('.confirm_btn');

async function add_profile() {
    var form_data = new FormData;
    let image = preview_profile_input.files[0]
    form_data.append('image', image)
    const result = await fetch(base_url + '/user/profile/upload', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: form_data,
    })
    if (result.ok) {
        location.reload()
    }
}