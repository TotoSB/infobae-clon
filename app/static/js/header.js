function showMenu(){
    var menu = document.getElementById('menu');
    menu.style.display = "flex";
    menu.style.alignItems = "start";
    menu.style.flexDirection = "column";

}

function hideMenu(){
    document.getElementById('menu').style.display = "none";
}

window.addEventListener('scroll', function() {
    if (window.scrollY > 0) {
        hideMenu();
    }
});