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
    methods: {
	loginWindow: () => {
	    popup = window.open('https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=<client_id>&redirect_url=http%3A%2F%2Flocalhost%3A5000%2Flogin&response_type=code&scope=Contacts.Read');
	    console.log(popup);
	}
    }
});

var contacs = new Vue({
    el: '#contacts',
    data: {
	contacts: null,
    }
});


$(document).ready(() => {
    var status = $.get('/status', (data) => app.message = data.status);

    setInterval(() => {
	console.log('Get status');
	$.get('/status', (data) => app.status.online = data.status);
	$.get('/contacts', (data) => contacts.contacts = data);
	console.log(app.status.online);
    }, 1000);
});
