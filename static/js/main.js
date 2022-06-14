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
const modal_background = document.querySelector('.upload_modal_background');
const upload_modal = document.querySelector('.upload_modal');

modal_background.addEventListener('click', function (e) {
    if (e.target.classList.contains('upload_modal_background')) {
        close_modal()
    }
})
function open_modal() {
    document.querySelector('.upload_modal_background').style.display = "flex"
    document.body.style.overflow = 'hidden';
    let modal_left_now = parseInt((window.innerWidth - 1100) / 2)
    let modal_top_now = parseInt((window.innerHeight - 800) / 2)
    let upload_modal_body = document.querySelector('.upload_modal');
    upload_modal_body.style.left = modal_left_now + "px";
    upload_modal_body.style.top = modal_top_now + "px";
}

function close_modal() {
    document.querySelector('.upload_modal_background').style.display = "none"
    document.body.style.overflow = 'auto';

}

upload_modal.addEventListener('dragover', function (e) {
    e.preventDefault();
})
upload_modal.addEventListener('dragleave', function (e) {
    e.preventDefault();
})
upload_modal.addEventListener('drop', function (e) {
    e.preventDefault();
    const data = e.dataTransfer;
    const input_file = document.querySelector('#input_file');
    input_file.files = data.files

    const upload_file_image = document.querySelector('.upload_file_image');
    const tmp_data = data
    const reader = new FileReader();
    reader.onload = () => {
        upload_file_image.innerHTML +=
            `
        <img class="um_preview_images" src="${reader.result}" style.background-size = "cover">
        `
    }
    reader.readAsDataURL(tmp_data.files[0])
    reader.close()
})

const tag_title_input = document.getElementById("input_tag_title");

function take_tag_title(tag_title, tag_id) {
    const tag_title_id = document.getElementById("input_tag_title_list_obj_" + tag_title);
    tag_title_input.value = tag_title_id.innerText;
    console.log(tag_title_input.value)

}

tag_title_input.addEventListener('input', function () {
    const tag_title_class = document.querySelectorAll('.input_tag_title_list > .input_tag_title_list_obj');
    var include_text = document.getElementById('input_tag_title').value;

    for (let i = 0; i < tag_title_class.length; i++) {
        tag_title_class[i].style.display = (tag_title_class[i].innerText.includes(include_text)) ? 'block' : 'none';
    }
})

const csrftoken = get_cookie('csrftoken')

const like_count = document.querySelector(".like_count")
async function like(post_id) {
    const like_button = document.querySelector('.heart_btn_' + post_id)
    const result = await fetch(base_url + '/post/like/' + post_id, {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Aceept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (result.ok) {
        if (like_button.classList.contains("bi-heart-fill")) {
            like_button.classList.replace('bi-heart-fill', 'bi-heart')
            like_count.innerText - parseInt(like_count.innerText) - 1
        } else {
            like_button.classList.replace('bi-heart', 'bi-heart-fill')
            like_count.innerText - parseInt(like_count.innerText) + 1
        }
    }
}
// 첫번째 모달 관련
const post_modal_background = document.querySelector('.bt_post_modal_background');
const post_modal = document.querySelector('.bt_post_modal');

post_modal_background.addEventListener('click', function (e) {
    if (e.target.classList.contains('bt_post_modal_background')) {
        close_post_modal()
    }
})
function open_post_modal(post_id) {
    document.querySelector('.bt_post_modal_background').style.display = "flex"
    document.body.style.overflow = 'hidden';
    console.log(post_id)

    let modal_top_now = parseInt((window.innerHeight - post_modal.clientHeight) / 2)
    let modal_left_now = parseInt((window.innerWidth - post_modal.clientWidth) / 2)
    let post_modal_body = document.querySelector('.bt_post_modal');
    post_modal_body.style.left = modal_left_now + "px";
    post_modal_body.style.top = modal_top_now + "px";
}

function close_post_modal() {
    document.querySelector('.bt_post_modal_background').style.display = "none"
    document.querySelector('.bt_pm_edit_post_modal').style.display = "none"
    document.body.style.overflow = 'auto';

}

// 수정 모달 관련
const edit_post_modal_background = document.querySelector('.bt_pm_edit_post_modal_background');
const edit_post_modal = document.querySelector('.bt_pm_edit_post_modal');

edit_post_modal_background.addEventListener('click', function (e) {
    if (e.target.classList.contains('bt_pm_edit_post_modal_background')) {
        close_edit_post_modal()
    }
})

function open_edit_post_content(post_id) {
    console.log(post_id)
    document.querySelector('.bt_pm_edit_post_modal_background').style.display = "flex"
    document.querySelector('#bt_pm_edit_post_modal_' + post_id).style.display = "flex"

    const bt_pm_b_button_body_text = document.getElementById('bt_pm_b_button_body_text_' + post_id);
    bt_pm_b_button_body_text.innerText = document.getElementById('bt_pb_pt_ct_comment_' + post_id).innerText;

    let edit_modal_top_now = parseInt((window.innerHeight - edit_post_modal.clientHeight) / 2)
    let edit_modal_left_now = parseInt((window.innerWidth - edit_post_modal.clientWidth) / 2)
    let edit_post_modal_body = document.querySelector('.bt_pm_edit_post_modal');
    edit_post_modal_body.style.left = edit_modal_left_now + "px";
    edit_post_modal_body.style.top = edit_modal_top_now + "px";
}



function close_edit_post_modal() {
    document.querySelector('.bt_pm_edit_post_modal_background').style.display = "none"
    document.querySelector('.bt_pm_edit_post_modal').style.display = "none"

}
