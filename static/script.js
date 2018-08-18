var popup = null;

var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello!',
        popup: null,
        status: {
            online: false,
        }
    },
    created: function(){
        this.getData();
    },
    methods: {
        loginWindow: function(){
            popup = window.open('https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=<client_id>&redirect_url=http%3A%2F%2Flocalhost%3A5000%2Flogin&response_type=code&scope=Contacts.Read%20offline_access', '_self');
            console.log(popup);
        },
        getData: function(){
            axios.get('/status').then(function(res){
                console.log(res);
                app.status.online = res.data.status;
            });
        }
    }
});




var contacts = new Vue({
    el: '#contacts',
    data: {
        contacts_info: null,
    },
    methods: {
        update: function(){
            $.get('/contacts', (data) => {
                if(data.data && data.data.length > 0){
                    this.contacts_info = data.data;
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
