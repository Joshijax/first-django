var modal = document.getElementById("sidebar");

function opensidebar() {
    //document.getElementById("sidebar").style.left = "0px";
    document.getElementById("sidebar").classList.toggle('active');
    //document.getElementById("toggle-btn").classList.toggle('active2');
    //document.getElementById("body").classList.toggle('body2');
}

function closesidebar() {
    document.getElementById("sidebar").classList.toggle('active');
    //document.getElementById("toggle-btn").classList.toggle('active2');
    //document.getElementById("body").classList.toggle('body2');
}






// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.classList.toggle('active');
        //document.getElementById("toggle-btn").classList.toggle('active2');
    }
}


