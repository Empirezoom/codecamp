let body = document.querySelector('body')
let osas = document.querySelector('.osas')
let icon = document.querySelector('.bi-moon-fill')

osas.addEventListener('click', ()=>{
    body.classList.toggle('dark')
    if(body.classList.contains('dark')){
        icon.classList.replace('bi-moon-fill', 'bi-sun-fill')
    }
    else{
        icon.classList.replace('bi-sun-fill', 'bi-moon-fill')
    }
})