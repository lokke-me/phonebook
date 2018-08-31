var popup = null;


Vue.component('call-button', {
    props: ['pNumber'],
    template: '<td>{{ number }}</td>'
});


Vue.component('contact-list', {
    props : ['contacts'],
    template: '<table class="table table-sm><contact-row v-for="contact in contacts" v-bind:contact="contact" v-bind:key="contact.displayName"></contact-row>'
});

Vue.component('contact-row',{
    props: ['contact'],
    template: '<tr><td> {{ contact.displayName }} </td></tr>'
});


Vue.component('c-list', {
    props: ['contacts'],
    template: '<div class="contact-list-header"> {{ contacts.length }} <c-single v-for="contact in contacts" v-bind:contact="contact" v-bind:key="contact.displayName"> </c-single> </div>'
});

Vue.component('c-single', {
    props: {
        contact: Object
    },
    template: '<div><span>{{ contact.displayName }}</span><c-phone-number v-for="phone in contact.phones" v-bind:key="phone" v-bind:phonenumber="phone"></c-phone-number></div>'
});


Vue.component('c-phone-number', {
    props: {
        phonenumber: String
    },
    template: '<span>{{ phonenumber }}</span>'
});

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
    data: function(){
        return {
            contacts_info: []
        }
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
