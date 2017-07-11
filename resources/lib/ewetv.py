# -*- coding: utf-8 -*-
import zapisession as zapi

class EWETV(zapi.ZapiSession):
    def __init__(self, username, password):
        zapi.ZapiSession.__init__(self, username, password)
        self.baseUrl = 'https://tvonline.ewe.de'
        self.serviceName = 'EWE TV Online'
        self.serviceId = 'ewetv'

    def announce(self):
        url = self.baseUrl + '/zapi/v2/session/hello'  
        params = {"client_app_token" : self.fetchAppToken(),
                  "uuid"    : "608e1694-11fa-4424-9607-ad49b227f245",
                  "lang"    : "de",
                  "app_version": "2.0.4",
                  "format"	: "json"}
        self.session.post(url, data=params, verify=False)
