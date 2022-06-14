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

function open_post_modal(post_nickname, user_nickname, post_id, content, user_id, is_following) {
    if (post_nickname === user_nickname) {
        let my_edit_modal = `
            <div class="bt_post_modal" id="bt_post_modal">
                <div class= bt_pm_title>${post_nickname}님의 게시물</div>
                <div class="bt_pm_body">
                    <div class="bt_pm_b_button_body">
                        <div class="bt_pm_b_bd_edit" onclick="open_edit_post_content('${user_nickname}', '${post_id}', '${content}', '${is_following}')">수정하기</div>
                        <div class="bt_pm_b_bd_delete"><a class="delete_color" href = "${base_url}/post/delete/${post_id}">삭제하기</a></div>
                        <div class="bt_pm_b_bd_close" onclick="close_post_modal()">닫기</div>
                    </div>
                </div>
            </div>`
        post_modal_background.innerHTML = my_edit_modal;

    }
    else {
        if (is_following === "True") {
            post_modal_background.innerHTML = `<div class="bt_post_modal" id="bt_post_modal">
            <div class= bt_pm_title>${post_nickname}님의 게시물</div>
            <div class="bt_pm_body">
                <div class="bt_pm_b_button_body">
                <div class="bt_pm_b_bd_follow"><a href="${base_url}/user/follow/${post_nickname}">팔로우 취소</a></div>
                    <div class="bt_pm_b_bd_close" onclick="close_post_modal()">닫기</div>
                </div>
            </div>`
        } else {
            post_modal_background.innerHTML = `<div class="bt_post_modal" id="bt_post_modal">
            <div class= bt_pm_title>${post_nickname}님의 게시물</div>
            <div class="bt_pm_body">
                <div class="bt_pm_b_button_body">
                <div class="bt_pm_b_bd_follow"><a href="${base_url}/user/follow/${post_nickname}">팔로우</a></div>
                    <div class="bt_pm_b_bd_close" onclick="close_post_modal()">닫기</div>
                </div>
            </div>`
        }
    }
    post_modal_background.style.display = "flex";
    document.body.style.overflow = 'hidden';

    let modal_top_now = parseInt((window.innerHeight - 400) / 2)
    let modal_left_now = parseInt((window.innerWidth - 400) / 2)
    let post_modal_body = document.querySelector('.bt_post_modal');
    post_modal_body.style.left = modal_left_now + "px";
    post_modal_body.style.top = modal_top_now + "px";
}

function close_post_modal() {
    document.querySelector('.bt_post_modal_background').style.display = "none"
    document.body.style.overflow = 'auto';

}

// 수정 모달 관련
const edit_post_modal_background = document.querySelector('.bt_pm_edit_post_modal_background');

edit_post_modal_background.addEventListener('click', function (e) {
    if (e.target.classList.contains('bt_pm_edit_post_modal_background')) {
        close_edit_post_modal()
    }
})

function open_edit_post_content(user_nickname, post_id, content, is_following) {

    let edit_post_modal_html =
        `<div class="bt_pm_edit_post_modal" id="bt_pm_edit_post_modal">
        <div class= bt_pm_title>${user_nickname}님의 게시물</div>
            <div class="bt_pm_body">
                <form id="edit_cotent_form_${post_id}" name="edit_cotent_form_${post_id}" type = "submit" action="${base_url}/post/home/recent/edit_content/${post_id}" class="edit_cotent_form" method="post" enctype="multipart/form-data">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                <div class="bt_pm_b_button_body">
                    <textarea name="edit_content_text" id="bt_pm_b_button_body_text_${post_id}" cols="60" rows="7" style=" resize: none; "placeholder = "${content}"></textarea>
                </div>
                </form>
                <div class="bt_pm_b_button">
                    <button form="edit_cotent_form_${post_id}" type="submit">수정하기</button>
                </div> 
            </div>
    </div>`

    edit_post_modal_background.innerHTML = edit_post_modal_html;


    edit_post_modal_background.style.display = "flex";

    // const bt_pm_b_button_body_text = document.getElementById('bt_pm_b_button_body_text');
    // bt_pm_b_button_body_text.innerText = document.getElementById('bt_pb_pt_ct_comment';

    let edit_text_post_modal_top_now = parseInt((window.innerHeight - 400) / 2)
    let edit_text_post_modal_left_now = parseInt((window.innerWidth - 400) / 2)
    let edit_text_post_modal_body = document.querySelector('.bt_pm_edit_post_modal');
    edit_text_post_modal_body.style.left = edit_text_post_modal_left_now + "px";
    edit_text_post_modal_body.style.top = edit_text_post_modal_top_now + "px";
}

function close_edit_post_modal() {
    document.querySelector('.bt_pm_edit_post_modal_background').style.display = "none"
    document.querySelector('.bt_pm_edit_post_modal').style.display = "none"
}


const main_profile_img = document.querySelector('.main_profile_img');
const profile_modal_wrapper = document.querySelector('.profile_modal_wrapper');
main_profile_img.addEventListener('click', function () {
    profile_modal_wrapper.style.display = 'block';
})

profile_modal_wrapper.addEventListener('click', function (e) {
    if (e.target.classList.contains('profile_modal_wrapper')) {
        profile_modal_wrapper.style.display = 'none';
    }
})