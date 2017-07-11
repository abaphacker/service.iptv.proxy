# -*- coding: utf-8 -*-
import zapisession as zapi

class Zattoo(zapi.ZapiSession):
    def __init__(self):
        zapi.ZapiSession.__init__(self, '', '')
#        self.baseUrl = 'https://zattoo.com'
#        self.serviceName = 'Zattoo'
#        self.serviceId = 'zattoo'

    def fetchAppToken(self):
        pass

    def announce(self):
        pass

    def isLoggedIn(self):
        return True

    def login(self):
        return True

    def getChannelUrl(self):
        return 'USTREAM URL'

    def getChannelList(self):
        return dict() #see channel_data in channellist.py

    def getLogoPath(self):
        return ''

