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


