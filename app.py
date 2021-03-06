from flask import Flask, request, render_template, make_response, jsonify, redirect
from oauth_token import Token
from contacts_api import Contacts_Api, ContactList
from yaml import load, Loader
import data_scheduler
import requests
import sys

app_name = __name__

app = Flask(__name__)

config = None

print(sys.argv)
config_file_name = "config.yaml"

if len(sys.argv) > 1:
    print("Using %s for config file" % sys.argv[1])
    config_file_name = sys.argv[1]

with open(config_file_name, "r") as config_file:
    config = load(config_file)

call_url = 'http://%s:%s@%s/cgi-bin/ConfigManApp.com?number=' % (
    config['phone_user'], config['phone_pwd'], config['phone_ip'])

contacts_api = Contacts_Api(config['client_secret'], config['client_id'])
contact_list = ContactList()
ds = None


def req_auth(code):
    # client_id = "<client_id>"
    # redirect_url = "http%3A%2F%2Flocalhost%3A5000%2Flogin"
    # client_secret = "<client_secret>"
    # grant_type = "authorization_code"

    # payload = {'grant_type': grant_type, 'client_id': client_id, 'client_secret': client_secret, 'code': code, 'redirect_url': redirect_url}
    # r = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=payload)
    # # print(r.json())
    # token = r.json()['access_token']
    # expires_in = r.json()['expires_in']
    # print(token)
    # return Token(r.json()['access_token'], r.json()['expires_in'])
    pass


def get_contacts(tk):
    if tk.active:
        auth_code = {'Authorization': 'Bearer %s' % tk.token}
        r = requests.get(
            'https://outlook.office.com/api/v2.0/me/contacts', headers=auth_code)
        print(r.text)

# landing page
# shows status of current connection state
@app.route('/')
def index():
    return render_template('index.html')

# after user pressed the login button
# also the endpoint for the oauth auth request
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login")
    if request.method == 'POST':
        # Got authentificated
        contacts_api.got_auth()
    elif request.method == 'GET':
        # Got code for requesting token
        contacts_api.got_code(request.args['code'])
        contacts_api.auth_with_code()
        return redirect("/static/index.html")

    return render_template('debug_auth.html', login_state=contacts_api.get_state())


@app.route('/tokeninfo')
def token_info():
    # context = dict()
    # context['login_state'] = login_state
    # context['token'] = token
    # context['expires_in'] = expires_in
    # return render_template('token_info.html', context=context)
    pass


@app.route('/phonebook.xml')
def phonebook():
    resp = make_response(contact_list.to_xml(), 200)
    resp.headers['Content-Type'] = 'application/xml'
    return resp


@app.route('/status')
def status():
    return jsonify(status=contacts_api.get_state())

@app.route('/contacts')
def get_contacts():
    if contact_list:
        data_to_send = list(filter(lambda x: len(x['phones']) > 0,
                                   contact_list.to_json()))
        return jsonify(data_to_send)
    else:
        return jsonify(None)

@app.route('/contacts-length')
def get_contact_length():
    if contact_list:
        return jsonify(data=contact_list.length())
    else:
        return jsonify(data=None)

@app.route('/call')
def call():
    phone_number = request.args.get('number', '')
    requests.get(call_url + phone_number)
    return "OK"

@app.route('/link')
def link():
    res = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
    res += "client_id=" + config['client_id'] + "&redirect_url="
    res += "http%3A%2F%2Flocalhost%3A5105%2Flogin"
    res += "&response_type=code&scope=Contacts.Read%20offline_access"
    return res


if __name__ == '__main__':
    ds = data_scheduler.Data_Scheduler(contacts_api, contact_list)
    ds.start()
    app.run(debug=True, host='0.0.0.0', port=5105)
