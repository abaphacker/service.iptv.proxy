# -*- coding: utf-8 -*-
import urllib
import xbmcaddon, xbmcvfs

addon = xbmcaddon.Addon()
host = addon.getSetting('host')
port = addon.getSetting('port')
path = addon.getSetting('playlist_path') + 'iptv_channels.m3u'

def buildUrl(query):
    url = 'http://' + host + ':' + port + '/channel.m3u8?'
    return url + urllib.urlencode(query)

def buildExtInfo(data, service_name=''):
    line = '#EXTINF:-1'
    line += ' tvg-id=%s.de' % (data['title'].replace(' ', ''))
#    line += ' tvg-logo=%s.de' % (data['title'].replace(' ', ''))
    line += ' tvg-logo=%s' % ('http://logos.zattic.com' + data['logo_black_84'])
    line += ' group-title="%s"' % (service_name)
    line += ' tvg-name=%s, %s' % (data['title'].replace(' ', ''), data['title'])
    return line

def generateM3U(tvservices):
    if len(tvservices)<1:
        return False

    m3u_lines = []
    has_changed = False

    if xbmcvfs.exists(path):
        f = xbmcvfs.File(path, 'r')
        m3u_lines = f.read().split('\n')
        f.close()

    for tvs in tvservices:
        channel_data = tvs.getChannelList()
        for group in channel_data['channel_groups']:
            for c in group['channels']:
                for quality in c['qualities']:
                    if not quality['availability'] in ['available', 'needs_internal_network']:
                        continue

                    line1 = buildExtInfo(quality, tvs.serviceName).encode('utf8')
                    line2 = buildUrl({'sid': tvs.serviceId, 'cid': c['cid']}).encode('utf8')
                    if not line1 in m3u_lines and not line2 in m3u_lines:
                        m3u_lines.append(line1)
                        m3u_lines.append(line2)
                        has_changed = True

    if addon.getSetting('m3u') == 'true':
        m3u_path = addon.getSetting('m3u_path')
        if xbmcvfs.exists(m3u_path):
            f = xbmcvfs.File(m3u_path, 'r')
            lines = f.read().split('\n')
            for l in lines:
                if not l.startswith('#EXTM3U') and l not in m3u_lines:
                    m3u_lines.append(l)
                    has_changed = True

    if has_changed:
        f = xbmcvfs.File(path, 'w+')
        if not m3u_lines[0].startswith('#EXTM3U'):
            f.write('#EXTM3U\n')
        for item in m3u_lines:
            if not item == '':
                f.write(item + '\n')
        f.close()

    del m3u_lines[:]
    return has_changed
