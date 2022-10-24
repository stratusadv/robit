document.addEventListener('alpine:init', () => {
    Alpine.data('monitor', () => ({
        data: {
        },
        start() {
            this.get_monitor_data()
            setInterval(() => {
                this.get_monitor_data()
            }, 2000)
        },

        async get_monitor_data() {
            let response = await fetch("monitor_api/");
            let responseText = await response.text();
            this.data = JSON.parse(responseText)
            console.log(this.data)
        },
    }))
})