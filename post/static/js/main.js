const modal_background = document.querySelector('.upload_modal_background');
const upload_modal = document.querySelector('.upload_modal');

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
    let upload_modal_body = document.querySelector('.upload_modal');
    upload_modal_body.style.left = modal_left_now + "px";
    upload_modal_body.style.top = modal_top_now + "px";
}

 function close_modal(){
    document.querySelector('.upload_modal_background').style.display="none"
    document.body.style.overflow = 'auto';
    
}

upload_modal.addEventListener('dragover', function(e){
    e.preventDefault();
})
upload_modal.addEventListener('dragleave', function(e){
    e.preventDefault();
})
upload_modal.addEventListener('drop', function(e){
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
        <img class="um_preview_images" src="${reader.result}">
        `
    }
    reader.readAsDataURL(tmp_data.files[0])
    reader.close()
})