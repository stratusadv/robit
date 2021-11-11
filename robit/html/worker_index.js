function Container() {
    return {
        data: {
            "groups": [],
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
            let job_list = document.getElementsByClassName("job-details")
            for (i = 0; i < job_list.length; i++) {
                job_list[i].style.display = 'none'
            }
            document.getElementById("job-" + id).style.display = 'block';
            let responseText = await response.text();
            // console.log(responseText)
            // this.totalVuePackages = data.total;
        }

    }
}

PetiteVue.createApp({
    Container,
}).mount()