function Container() {
    return {
        name: '',
        health: '',
        job_list: [],

        get_json_data(json_data) {
            this.name = json_data.name
            this.health = json_data.average_job_health
            this.job_list = json_data.job_list
            console.log(this.job_list[1].health)
        },

        ajax_json_request() {
            const xmlHttp = new XMLHttpRequest();
            let get_json_data = this.get_json_data

            xmlHttp.onreadystatechange = function () {
                if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
                    get_json_data(JSON.parse(this.responseText))
                }
            }

            xmlHttp.open("GET", 'api');
            xmlHttp.send();
        },

    }
}

PetiteVue.createApp({
    Container,
}).mount();