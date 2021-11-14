function Container() {
    return {
        data: {
            "groups": [],
            "clock": {}
        },

        job_details: {

        },

        start() {
            this.get_worker_data()
            setInterval(this.get_worker_data, 2000)
            setTimeout(function () {
                document.getElementById("loading").classList.add("d-none");
                document.getElementById("loading").classList.remove("d-block");
                document.getElementById("container").classList.remove("d-none");
            }, 500)
        },

        async get_worker_data() {
            let response = await fetch("worker_api/");
            let responseText = await response.text();
            this.data = JSON.parse(responseText)
        },

        async get_job_details(id) {
            let response = await fetch("job_api/" + id);
            let job = document.getElementById("job-" + id)
            if (job.style.display === 'block') {
                job.style.display = 'none'
            } else {
                job.style.display = 'block'
            }
            let responseText = await response.text();
            let json_data = JSON.parse(responseText)
            this.job_details[json_data.job_detail.id] = json_data.job_detail
        }

    }
}

PetiteVue.createApp({
    Container,
}).mount()