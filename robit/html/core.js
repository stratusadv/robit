function hide_loading() {
    setTimeout(function () {
        document.getElementById("loading").classList.add("d-none");
        document.getElementById("loading").classList.remove("d-block");
        document.getElementById("container").classList.remove("d-none");
    }, 500)

}