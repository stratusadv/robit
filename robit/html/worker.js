document.addEventListener('alpine:init', () => {
    Alpine.data('worker', () => ({
        data: {
            "groups": [],
            "clock": {}
        },

        job_details: {},

        job_results: {},

        init() {
            this.get_worker_data()
            setInterval(() => {
                this.get_worker_data()
            }, 1000)
        },

        async get_worker_data() {
            let response = await fetch("api/worker/");
            let responseText = await response.text();
            this.data = JSON.parse(responseText)
        },

        async get_job_details(id) {
            let response = await fetch("api/job/" + id);
            let job = document.getElementById("job-" + id)
            if (job.style.display === 'block') {
                job.style.display = 'none'
            } else {
                job.style.display = 'block'
            }
            let responseText = await response.text();
            let json_data = JSON.parse(responseText)
            this.job_details[json_data.job_detail.id] = json_data.job_detail
        },

        async get_job_results(id) {
            let response = await fetch("api/job_results/" + id);
            // let job_results_modal_body = document.getElementById("job-results-modal-body")
            let responseText = await response.text();
            this.job_results = JSON.parse(responseText)
        }


    }))
})

