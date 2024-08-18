function showMenuUser(){
    var menu = document.getElementById('menu-user');

    if (window.innerWidth < 450) {
        menu.style.width = '100%';
        const enlaces = menu.querySelectorAll('a');
        enlaces.forEach(enlace => {
            enlace.style.marginLeft = "20px"
        });
    }

    menu.style.display = "flex";
    menu.style.flexDirection = "column";
}

function hideMenUser(){
    var menu = document.getElementById('menu-user');
    menu.style.display = "none";
}

window.addEventListener('scroll', function() {
    if (window.scrollY > 0) {
        hideMenUser();
    }
});