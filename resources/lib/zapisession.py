# -*- coding: utf-8 -*-
import os
import requests
import re
import pickle
import xbmc, xbmcaddon

addon = xbmcaddon.Addon()

class ZapiSession:
    def __init__(self, username, password):
        self.baseUrl = ''
        self.serviceName = ''
        self.cookie_path = xbmc.translatePath(addon.getAddonInfo('profile')) + '/cookies_'
        self.serviceId = ''
        self.serviceName = ''
        self.session = requests.Session()
        self.session.headers["User-Agent"] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        self.username = username
        self.password = password
        self.account_data = None
        self.current_channel_id = ''

    def fetchAppToken(self):
        r = requests.get(self.baseUrl, verify=False)
        html = r.text
        return re.search("window\.appToken\s*=\s*'(.*)'", html).group(1)

    def announce(self):
        pass

    def isLoggedIn(self):
        self.cookie_path += self.serviceId
        if os.path.isfile(self.cookie_path):
            with open(self.cookie_path) as f:
                cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
                self.session.cookies = cookies

        url = self.baseUrl + '/zapi/v2/session'
        r = self.session.get(url, verify=False)
        data = r.json()
        print r.text
        if data['success'] == 'true':
            if data['session']['loggedin'] == 'true':
                self.account_data = data
                return True

        self.session.cookies.clear()
        return False

    def login(self):
        if self.isLoggedIn():
            return True

        self.announce()
        url = self.baseUrl + '/zapi/v2/account/login'
        headers = self.session.headers
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        payload = {'login': self.username, 'password': self.password, 'remember': 'true'}
        r = self.session.post(url, data=payload, headers=headers, verify=False)
        data = r.json()
        if data['success']:
            self.account_data = data
            with open(self.cookie_path, 'w') as f:
                    pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
            return True

        return False

    def getChannelUrl(self):
        url = self.baseUrl + '/zapi/watch'
        headers = self.session.headers
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        params = {'cid': self.current_channel_id, 'stream_type': 'hls'}
        r = self.session.post(url, data=params, headers=headers, verify=False)
        return r.json()["stream"]["url"]

    def getChannelList(self):
        url = self.baseUrl + '/zapi/v2/cached/channels/' + self.account_data['session']['power_guide_hash'] + '?details=False'
        headers = self.session.headers
        r = self.session.get(url, headers=headers, verify=False)
        data = r.json()
        if data['success']:
            return data

        return None

    def getLogoPath(self):
        if self.account_data:
            return self.account_data['session']['logo_base_url'] + '/' + self.account_data['session']['power_guide_hash'] + '/'

