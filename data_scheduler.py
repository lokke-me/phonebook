import threading
import time


class Data_Scheduler(threading.Thread):
    def __init__(self, ca, contact_list):
        threading.Thread.__init__(self)
        self.ca = ca
        self.contact_list = contact_list

    def run(self):
        print("Run data thread")
        while(True):
            if self.ca.get_state():
                self.ca.get_contacts(self.contact_list)
                print("Items: " + str(self.contact_list.length()))

            time.sleep(60)
