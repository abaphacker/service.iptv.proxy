# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon
import SimpleHTTPServer
import SocketServer
import urlparse
import resources.lib.ewetv as ewetv
import resources.lib.zattoo as zattoo
import resources.lib.netcologne as netcologne
import channellist

addon = xbmcaddon.Addon()
host = addon.getSetting('host')
port = int(addon.getSetting('port'))

channels_file = addon.getSetting('playlist_path') + 'iptv_channels.m3u'
plugin_path = xbmc.translatePath(addon.getAddonInfo('path'))

tv_services = []
#Kodi < v17 workaround
redirect_url = ''

class httpHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        global redirect_url
        p = urlparse.urlparse(self.path)
        params = urlparse.parse_qs(p.query)
        if p.path == '/channel.m3u8':
            if 'sid' in params:
                for tvs in tv_services:
                    if tvs.serviceId == params['sid'][0]:
                        tvs.current_channel_id = params['cid']
                        redirect_url = tvs.getChannelUrl()
                        break

        self.send_response(301)
        self.send_header('Location', redirect_url)
        self.end_headers()

if addon.getSetting('ewetv') == 'true':
    ewetv = ewetv.EWETV(addon.getSetting('user_ewe'), addon.getSetting('pass_ewe'))
    if ewetv.login():
        tv_services.append(ewetv)
if addon.getSetting('netcologne') == 'true':
    nc = netcologne.NetCologne(addon.getSetting('user_nc'), addon.getSetting('pass_nc'))
    if nc.login():
        tv_services.append(nc)
if addon.getSetting('zattoo') == 'true':
    zattoo = zattoo.Zattoo(addon.getSetting('user_zattoo'), addon.getSetting('pass_zattoo'))
    if zattoo.login():
        tv_services.append(zattoo)

if len(tv_services)>0:
    print tv_services    
    if channellist.generateM3U(tv_services):
        xbmcgui.Dialog().notification('IPTV Proxy', 'Senderliste aktualisiert. Neustart erforderlich!', xbmcgui.NOTIFICATION_INFO, 5000, True)
    xbmc.log('Starting IPTV Proxy on port ' + str(port))
    SocketServer.TCPServer.allow_reuse_address = True
    handler = SocketServer.TCPServer((host, port), httpHandler)
    handler.serve_forever()
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            handler.shutdown()
            break

