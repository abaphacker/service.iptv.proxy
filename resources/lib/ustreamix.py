# -*- coding: utf-8 -*-
import zapisession as zapi
import ustreamix_api as uapi

class Ustreamix(zapi.ZapiSession):
    def __init__(self):
        zapi.ZapiSession.__init__(self, '', '')
        self.baseUrl = 'http://v2.ustreamix.?'
        self.serviceName = 'Ustreamix'
        self.serviceId = 'Ustreamix'

    def fetchAppToken(self):
        pass

    def announce(self):
        pass

    def isLoggedIn(self):
        return True

    def login(self):
        return True

    def getChannelUrl(self):
        return uapi.getStream(self.current_channel_id[0])

    def getChannelList(self):
        channel_list = { 'channel_groups': [ { 'channels' : [ ] }] } 
        channel = self.getChannelItem('pro-7')
        channel_list[ 'channel_groups'][0]['channels'].append(channel)
        channel = self.getChannelItem('rtl-de')
        channel_list[ 'channel_groups'][0]['channels'].append(channel)
        return channel_list #see channel_data in channellist.py

    def getLogoPath(self):
        return ''

    def getChannelItem( self, name ):
        chan = { 'cid': name ,'qualities' : [ { 'availability': 'available', 'title': name, 'logo_black_84': '' } ] }
        return chan
