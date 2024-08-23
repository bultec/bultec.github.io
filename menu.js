function changeclass(event) {
    event.preventDefault();
    document.body.classList.toggle("with--sidebar");
}

var icon=document.getElementById("header_icon");
icon.addEventListener("click",changeclass,false);
