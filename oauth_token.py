import requests
import pprint

pp = pprint.PrettyPrinter()


class Contact():
    def __init__(self, contactDict):
        self.displayName = contactDict['DisplayName']
        self.companyName = contactDict['CompanyName']

        self.phones = []

        self.preparePhones(contactDict['BusinessPhones'])
        self.preparePhones(contactDict['HomePhones'])
        if contactDict['MobilePhone1']:
            self.phones.append(self.sanitizePhoneNo(
                contactDict['MobilePhone1']))

    def __str__(self):
        return "{} - {} - {}".format(self.displayName, self.companyName, " ".join(self.phones))

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


class ContactList:
    def __init__(self):
        self.list = []

    def append(self, values):
        for item in values:
            self.list.append(Contact(item))

    def dump(self):
        for contact in self.list:
            pp.pprint(str(contact))


class Token:
    def __init__(self):
        self.token = None
        self.expires_in = None
        self.active = False
        self.code = None
        self.access_token = None

    def get_token(self):
        return self.token

    def get_expiration(self):
        return self.expires_in

    def set_active(self):
        self.active = True

    def set_disabled(self):
        self.active = False

    def get_state_str(self):
        if self.active:
            return "active"
        else:
            return "inactive"

    def get_state(self):
        return self.active

    def __str__(self):
        return "Token: %s, expires in: %s, currently %s" % (str(self.token), str(self.expires_in), self.get_state_str())

    def got_code(self, code):
        self.code = code

    def got_access_token(self, access_token):
        self.access_token = access_token


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
        payload = {'grant_type': self.grant_type,
                   'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'code': self.token.code,
                   'redirect_url': self.redirect_url}

        r = requests.post(
            'https://login.microsoftonline.com/common/oauth2/v2.0/token', data=payload)
        if r.status_code == 200:
            # success
            data = r.json()
            self.token.access_token = data['access_token']
            self.token.active = True
            self.token.expires_in = data['expires_in']
            print(self.token.access_token)
        else:
            print("ERROR: could not authorize access token")
            r.raw

    def got_code(self, code):
        self.token.got_code(code)

    def got_auth(self):
        pass

    def get_state(self):
        print(self.token.get_state_str())
        return self.token.get_state()

    def tt(self):
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

        return cl
