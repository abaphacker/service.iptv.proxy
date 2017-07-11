# -*- coding: utf-8 -*-
import zapisession as zapi

class Zattoo(zapi.ZapiSession):
    def __init__(self, username, password):
        zapi.ZapiSession.__init__(self, username, password)
        self.baseUrl = 'https://zattoo.com'
        self.serviceName = 'Zattoo'
        self.serviceId = 'zattoo'

    def announce(self):
        url = self.baseUrl + '/zapi/session/hello'
        params = {"client_app_token" : self.fetchAppToken(),
                  "uuid"    : "9518635d-2994-4be6-a567-f4ef875ff672",
                  "lang"    : "de",
                  "format"	: "json"}
        self.session.post(url, data=params, verify=False)

