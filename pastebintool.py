from pastebin import PastebinAPI
from xml.etree import cElementTree as ET
import time


class ieatpaste:
    def __init__(self, _body=None, _title=None, _filetoread=None):
        self.DEVKEY = ''
        self.TITLE = _title
        self.BODY = _body
        self.password = ''
        self.username = ''
        self.apiobject = PastebinAPI()
        self.filetoread = _filetoread
        self.userkey = self.apiobject.generate_user_key(api_dev_key=self.DEVKEY,
                                                        username=self.username,
                                                        password=self.password)
        self.pastekeys = []

    def loadthefile(self):
        try:
            with open(self.filetoread, 'r+') as file:
                self.TITLE = '{}-stamped'.format(int(time.time()))
                self.BODY = file.read()
                file.truncate()
                file.close()
        except Exception as E:
            self.BODY = E
            pass

    def dothepaste(self):
        try:
            self.apiobject.paste(api_dev_key=self.DEVKEY, api_user_key=self.userkey, api_paste_code=self.BODY,
                                 paste_private='private', paste_name=self.TITLE)
        except Exception as E:
            print E

    def listpastes(self):
        try:
            x = self.apiobject.pastes_by_user(api_dev_key=self.DEVKEY, api_user_key=self.userkey)

            x = x.split("</paste>")
            x = [y + "</paste>\r\n" for y in x]

            for key in x[:-1]:
                paste = ET.fromstring(key)
                self.pastekeys.append(paste.find('paste_key').text)
                # print self.pastekeys
        except Exception as E:
            print E

    def deletepastes(self):
        if self.pastekeys:
            for i in self.pastekeys:
                print i
                self.apiobject.delete_paste(api_dev_key=self.DEVKEY, api_user_key=self.userkey, api_paste_key=i)


def main():
    x = ieatpaste()
    # x.filetoread='/var/log/snoopy.log'
    # x.loadthefile()
    # x.dothepaste()


    # while True:
    #   x.listpastes()
    #   x.deletepastes()


main()
