function Container() {
    return {
        data: {
            "groups": [],
        },

        job_details: {

        },

        get_json_data(json_data) {
            this.data = json_data
        },

        ajax_json_request() {
            const xmlHttp = new XMLHttpRequest()
            let get_json_data = this.get_json_data

            xmlHttp.onreadystatechange = function () {
                if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
                    get_json_data(JSON.parse(this.responseText))
                }
            }

            xmlHttp.open("GET", 'worker_api/');
            xmlHttp.send();
        },

        start() {
            this.ajax_json_request()
            setInterval(this.ajax_json_request, 2000)
            setTimeout(function () {
                document.getElementById("loading").classList.add("d-none");
                document.getElementById("loading").classList.remove("d-block");
                document.getElementById("container").classList.remove("d-none");
            }, 500)
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
            // console.log(JSON.stringify(this.job_details))
        }

    }
}

PetiteVue.createApp({
    Container,
}).mount()