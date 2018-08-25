var popup = null;

var app = new Vue({
    el: '#app',
    data: {
        status: {
            online: false,
        },
        link: null
    },
    created: function(){
        this.getStatus();
        this.getLink();
    },
    methods: {
        loginWindow: function(){
            window.open(app.link, '_self');
        },
        getStatus: function(){
            axios.get('/status').then(function(res){
                console.log(res.data);
                app.status.online = res.data.status;
            });
        },
        getLink: function(){
            axios.get('/link').then(function(res){
                console.log(res.data);
                app.link = res.data;
            });
        }
    }
});




var contacts = new Vue({
    el: '#contacts',
    data: {
        contacts_info: [],
    },
    created: function(){
        this.update();
    },
    methods: {
        update: function(){
            axios.get('/contacts').then(function(res){
                if(res && res.data && res.data.length > 0){
                    console.log(res.data);
                    contacts.contacts_info = res.data;
                }
            });
        }
    }
});


//$(document).ready(() => {
//    contacts.update();
//    setInterval(() => {
//      console.log('Get status');
//      $.get('/status', (data) => app.status.online = data.status);
//    }, 10000);
//});
