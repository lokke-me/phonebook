import requests
import pprint
from oauth_token import Token

pp = pprint.PrettyPrinter()


class Contacts_Api():
    def __init__(self):
        self.client_secret = "<client_secret>"
        self.client_id = "<client_id>"
        self.redirect_url = "http%3A%2F%2Flocalhost%3A5000%2Flogin"
        self.token_request_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        self.grant_type = 'authorization_code'
        self.token = Token()
        self.response_type = 'code'
        self.scope = 'Contacts.Read%20offline_access'
        self.load_savedata()

    def load_savedata(self):
        try:
            with open("./persist/savedata", "r") as f:
                line = f.readline()
                print("Token from save:")
                print(line)
                if len(line) > 0:
                    self.token.set_refresh_token(line)
                    self.auth_with_refresh_token()
        except FileNotFoundError:
            print("No persistend data found")

    def save_token(self):
        with open("./persist/savedata", "w") as f:
            f.write(self.token.refresh_token)
            f.write("\n")

    def auth_with_code(self):
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
            'https://login.microsoftonline.com/common/oauth2/v2.0/token',
            data=payload)
        if r.status_code == 200:
            # success
            print("Successfully authentificated")
            data = r.json()
            self.token.access_token = data['access_token']
            self.token.set_refresh_token(data['refresh_token'])
            self.token.active = True
            self.token.expires_in = data['expires_in']
            # print("Token: " + self.token.access_token)
            print(r.text)
            self.save_token()
        else:
            print("ERROR: could not authorize access token")
            r.raw

        print("End authentification")

    def auth_with_refresh_token(self):
        # forword of oauth login
        # contains request token
        # request auth token
        # save auth token
        # start trigger to refresh token automatically
        print("Start authentification")
        payload = {'grant_type': "refresh_token",
                   'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'refresh_token': self.token.refresh_token,
                   'redirect_url': self.redirect_url}

        r = requests.post(
            'https://login.microsoftonline.com/common/oauth2/v2.0/token',
            data=payload)
        if r.status_code == 200:
            # success
            print("Successfully authentificated")
            data = r.json()
            self.token.access_token = data['access_token']
            self.token.set_refresh_token(data['refresh_token'])
            self.token.active = True
            self.token.expires_in = data['expires_in']
            # print("Token: " + self.token.access_token)
            print(r.text)
            self.save_token()
        else:
            print("ERROR: could not authorize access token")
            r.raw

        print("End authentification")

    def got_code(self, code):
        self.token.got_code(code)

    def got_auth(self):
        pass

    def get_state(self):
        # print(self.token.get_state_str())
        return self.token.get_state()

    def get_contacts(self, contact_list):
        print("Start dump")
        contact_list.clear()
        auth = {'Authorization': 'Bearer {}'.format(self.token.access_token)}
        r = requests.get(
            'https://graph.microsoft.com/v1.0/me/contacts', headers=auth)

        if r.status_code == 200:
            res_data = r.json()
            contact_list.append(res_data['value'])
            # print(r.json())
            while '@odata.nextLink' in res_data:
                # print(str(res_data))
                r = requests.get(res_data['@odata.nextLink'], headers=auth)
                res_data = r.json()
                contact_list.append(res_data['value'])

        else:
            print("(%s) Could not fetch contacts" % str(r.status_code))
            self.auth_with_refresh_token()


class ContactList:
    def __init__(self):
        self.list = []

    def append(self, values):
        print("Append: " + str(len(self.list)))
        for item in values:
            self.list.append(Contact(item))

    def dump(self):
        for contact in self.list:
            pp.pprint(str(contact))

    def get_all(self):
        return self.list

    def length(self):
        return len(self.list)

    def clear(self):
        self.list.clear()

    def to_json(self):
        result = []
        for item in self.list:
            result.append(item.to_dict())

        return result


class Contact():
    def __init__(self, contactDict):
        self.displayName = "%s, %s" % (contactDict['surname'], contactDict['givenName'])
        self.companyName = contactDict['companyName']

        self.phones = []

        self.preparePhones(contactDict['businessPhones'])
        self.preparePhones(contactDict['homePhones'])
        print(contactDict)

    def __str__(self):
        return "{} - {} - {}".format(self.displayName, self.companyName,
                                     " ".join(self.phones))

    def sanitizePhoneNo(self, rawPhone):
        rawPhone = str(rawPhone).replace("+49", "0")
        rawPhone = rawPhone.replace("-", "")
        rawPhone = rawPhone.replace("/", "")
        rawPhone = rawPhone.replace("(", "")
        rawPhone = rawPhone.replace(")", "")
        rawPhone = rawPhone.replace(" ", "")
        rawPhone = rawPhone.replace("–", "")
        print(rawPhone)
        return rawPhone

    def preparePhones(self, phones):
        for phone in phones:
            self.phones.append(self.sanitizePhoneNo(phone))

    def to_dict(self):
        return {'displayName': self.displayName,
                'companyName': self.companyName, 'phones': self.phones}
