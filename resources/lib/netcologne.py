# -*- coding: utf-8 -*-
import zapisession as zapi

class NetCologne(zapi.ZapiSession):
    def __init__(self, username, password):
        zapi.ZapiSession.__init__(self, username, password)
        self.baseUrl = 'https://nettv.netcologne.de'
        self.serviceName = 'NetCologne NetTV Go'
        self.serviceId = 'netcologne'

    def announce(self):
        url = self.baseUrl + '/zapi/v2/session/hello'  
        params = {"client_app_token" : self.fetchAppToken(),
                  "uuid"    : "75d01ba8-3c52-406d-a322-4b9eec1efb07",
                  "lang"    : "de",
                  "app_version": "2.1.0",
                  "format"	: "json"}
        self.session.post(url, data=params, verify=False)
