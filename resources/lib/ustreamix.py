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
        channel_list = { 'channel_groups': [ { 'channels' : [ ] }] } 
        chanel = self.getChannelItem('RTL-2')
        channel_list[ 'channel_groups'][0]['channels'].append(channel)
        return dict() #see channel_data in channellist.py

    def getLogoPath(self):
        return ''

    def getChannelItem( self, name ):
        chan = { 'cid': name ,'qualities' : [ { 'availability': 'available', 'title': name, 'logo_black_84': '' } ] }
        return chan