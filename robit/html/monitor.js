function Container() {
    return {
        data: {
            "workers": [],
            "clock": {}
        },

        start() {
            this.get_monitor_data()
            setInterval(this.get_monitor_data, 2000)
            setTimeout(function () {
                document.getElementById("loading").classList.add("d-none");
                document.getElementById("loading").classList.remove("d-block");
                document.getElementById("container").classList.remove("d-none");
            }, 500)
        },

        async get_monitor_data() {
            let response = await fetch("monitor_api/");
            let responseText = await response.text();
            this.data = JSON.parse(responseText)
        },

    }
}

PetiteVue.createApp({
    Container,
}).mount();