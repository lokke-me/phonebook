import requests
from oauth_token import Token


class Contacts_Api():
    def __init__(self):
        self.client_secret = "<client_secret>"
        self.client_id = "<client_id>"
        self.redirect_url = "http%3A%2F%2Flocalhost%3A5000%2Flogin"
        self.token_request_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        self.grant_type = 'authorization_code'
        self.token = Token()
        self.response_type = 'code'
        self.scope = 'Contacts.Read'

    def auth(self):
        # forword of oauth login
        # contains request token
        # request auth token
        # save auth token
        # start trigger to refresh token automatically
        print("Start authentification")
        payload = {'grant_type': self.grant_type,
                   'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'code': self.token.code,
                   'redirect_url': self.redirect_url}

        r = requests.post(
            'https://login.microsoftonline.com/common/oauth2/v2.0/token', data=payload)
        if r.status_code == 200:
            # success
            print("Successfully authentificated")
            data = r.json()
            self.token.access_token = data['access_token']
            self.token.active = True
            self.token.expires_in = data['expires_in']
            print("Token: " + self.token.access_token)
            print(r.text)
        else:
            print("ERROR: could not authorize access token")
            r.raw

        print("End authentification")

    def got_code(self, code):
        self.token.got_code(code)

    def got_auth(self):
        pass

    def get_state(self):
        print(self.token.get_state_str())
        return self.token.get_state()

    def tt(self):
        print("Start dump")
        cl = ContactList()
        auth = {'Authorization': 'Bearer {}'.format(self.token.access_token)}
        r = requests.get(
            'https://outlook.office.com/api/v2.0/me/contacts', headers=auth)

        if r.status_code == 200:
            res_data = r.json()
            cl.append(res_data['value'])
            print(r.json())
            while '@odata.nextLink' in res_data:
                print(str(res_data))
                r = requests.get(res_data['@odata.nextLink'], headers=auth)
                res_data = r.json()
                cl.append(res_data['value'])
        else:
            print("Return code: " + str(r.status_code))
            print(r.text)

        return cl


class ContactList:
    def __init__(self):
        self.list = []

    def append(self, values):
        for item in values:
            self.list.append(Contact(item))

    def dump(self):
        for contact in self.list:
            pp.pprint(str(contact))
