const modal_background = document.querySelector('.upload_modal_background');
const small_modal = document.querySelector('.upload_modal');

modal_background.addEventListener('click', function (e) {
if (e.target.classList.contains('upload_modal_background')) {
    close_modal()
}
})
function open_modal(){
    document.querySelector('.upload_modal_background').style.display="block"
    document.body.style.overflow = 'hidden';
    let modal_top_now = parseInt((window.innerHeight - 380) / 2)
    let modal_left_now = parseInt((window.innerWidth - 380) / 2)
    let small_modal_body = document.querySelector('.upload_modal');
    small_modal_body.style.left = modal_left_now + "px";
    small_modal_body.style.top = modal_top_now + "px";
    small_modal.style.display = 'flex';
    small_modal.style.justifycontent = 'center';
    small_modal.style.alignitems = "center"; 
}

 function close_modal(){
    document.querySelector('.upload_modal_background').style.display="none"
    document.querySelector('.upload_modal').style.display="none"
    document.body.style.overflow = 'auto';
}