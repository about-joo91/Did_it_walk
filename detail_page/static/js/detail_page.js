let dc_comment_box = document.querySelectorAll('.dc_comment_box')
let is_visible_all = dc_comment_box.length > 3;
const more_btn = document.querySelector('.more_btn')
const dc_comment_box_wrapper = document.getElementById('dc_comment_box_wrapper')
if (is_visible_all) {
    more_btn.style.display = 'block';
    dc_comment_box_wrapper.innerHTML = ''
    for (let i = 0; i < 3; i++) {
        dc_comment_box_wrapper.append(dc_comment_box[i]);
    }
} else {
}

more_btn.addEventListener('click', function () {
    dc_comment_box_wrapper.append(...dc_comment_box);
    more_btn.style.display = 'none';
})
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
const like_button = document.querySelector('.heart_btn')
const dc_ch_b_leng = document.querySelector('.dc_ch_b_leng')
async function like(post_id) {
    const result = await fetch(base_url + '/post/like/' + post_id, {
        method: 'POST',
        headers: {
            'Aceept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (result.ok) {
        if (like_button.classList.contains("bi-heart-fill")) {
            like_button.classList.replace('bi-heart-fill', 'bi-heart')
            dc_ch_b_leng.innerText = parseInt(dc_ch_b_leng.innerText) - 1
        } else {
            like_button.classList.replace('bi-heart', 'bi-heart-fill')
            dc_ch_b_leng.innerText = parseInt(dc_ch_b_leng.innerText) + 1
        }
    }
}

const comment_form = document.getElementById('comment_form')

comment_form.addEventListener('submit', function (e) {
    if (document.getElementById('comment_input').value == '') {
        alert('댓글을 적어주세요!')
        e.preventDefault();
    }
})

async function comment_delete(post_id, comment_id) {
    const result = await fetch(base_url + '/post/comment/' + post_id + '/' + comment_id, {
        method: 'POST',
        headers: {
            'Aceept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (result.ok) {
        location.reload()
    }
}

function edit_ready(comment_id, content) {
    const dc_cb_content_box = document.getElementById('dc_cb_content_box_' + comment_id)
    dc_cb_content_box.innerHTML = `
    <form method="post" action="${base_url}/post/comment/edit/${comment_id}" type="submit" name="comment_edit_form${comment_id}" id="comment_edit_form${comment_id}">
    <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
    <textarea name="edit_box" class="edit_box" id = "new_content_${comment_id}" placeholder="${content}"></textarea>
    </form>`
    const dc_cb_button_box = document.getElementById('dc_cb_button_box_' + comment_id)
    dc_cb_button_box.innerHTML = `<button class="edit_submit_btn" type="submit" form="comment_edit_form${comment_id}">확인</button>`
}


