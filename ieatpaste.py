from pastebin import PastebinAPI
import time

class ieatpaste:
    def __init__(self, _body=None, _title=None):
        self.DEVKEY = ''
        self.TITLE = _title
        self.BODY = _body
        self.password = ''
        self.username = ''
        self.apiobject = PastebinAPI()
        self.userkey = self.apiobject.generate_user_key(api_dev_key=self.DEVKEY,
                                                        username=self.username,
                                                        password=self.password)

    def dothepaste(self):
        try:
            self.apiobject.paste(api_dev_key=self.DEVKEY, api_user_key=self.userkey, api_paste_code=self.BODY,
                                 paste_private='private', paste_name=self.TITLE)
        except Exception as E:
            print E


def main():
    with open('/home/zahats/testy.txt', 'r+' ) as file:
        x = ieatpaste()
        x.TITLE = '{}-hotcarled'.format(int(time.time()))
        x.BODY = file.read()
        x.dothepaste()

main()
