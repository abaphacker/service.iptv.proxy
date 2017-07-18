import re
import base64
import urllib2


def unObfuscate(chunks, number2subst):
    result = ''
    for ch in chunks:
        encoded = base64.b64decode(ch)
        num = re.sub('\D', '', encoded)
        num2 = int(num) - number2subst
        result += ''.join(map(unichr, [num2]))

    return result

def getToken(ownIp, channel):
    token_url = 'http://tmg.ustreamix.com/stats.php?p='  + ownIp + '&C=&Ket=live'
    #print url
    req = urllib2.Request(token_url)
    req.add_header('Referer', 'http://v2.ustreamix.com/stream.php?id=' + channel)
    tokenjson = urllib2.urlopen(req).read()
    #print tokenjson
    token_arr = re.findall('jdtk="(.*?)"', tokenjson)
    return token_arr[0]



def getStream(channel):
    url = 'http://v2.ustreamix.com/stream.php?id=' + channel
    f = urllib2.urlopen('http://v2.ustreamix.com/stream.php?id=' + channel)
    txt = f.read()

    #get ownIP
    own_ip = re.findall("var x_first_ip = '(.*?)';", txt)[0]

    number2subst = re.findall( '\) - (\d*)\); } \);', txt)[0]

    #get Obfuscated Chunks
    m = re.findall( '<script>.*\[(.*)\].*</script>', txt, re.DOTALL)
    chunks = re.findall('"(.*?)"', m[0] )

    decodedText = unObfuscate( chunks, int(number2subst) )
    #aus chara var stream = '....' lesen
    stream_url = re.findall("var stream = '(.*?)'", decodedText)[0]

    token = getToken( own_ip, channel )

    stream_url += token
    #print stream_url
    return stream_url


def listStreams():
    html = urllib2.urlopen('http://v2.ustreamix.com/').read()
    m = re.findall('stream.php\?id=(.*?)" target="_blank">(.*?)<span',html, re.DOTALL)
    #print m[0][0]
    return m
