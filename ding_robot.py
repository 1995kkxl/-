#!/usr/bin/python3
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import sys
import getopt
import codecs

#参数
webhook = ''
secret =  ''

def url_sign_robot():
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    url = "{webhook}&timestamp={timestamp}&sign={sign}".format(webhook=webhook,timestamp=timestamp, sign=sign)
    return url


def pack_conent(conent, type='text', mobiles=[]):
    data = {
        "msgtype": type,
        "text": {
            "content": conent
        },
        "at": {
            "atMobiles": [*mobiles],
            "isAtAll": False
        }
    }
    return data


def usage():
    print('--- 使用错误: {} -t <title> -v <verbose>'.format(sys.argv[0]))
    print('--- 或者: {} --title=<title> --verbose=<verbose>'.format(sys.argv[0]))


def run():
    title = ''
    verbose = ''
    try:
        options, args = getopt.getopt(sys.argv[1:], "ht:v:", longopts=['help', 'title=', 'verbose='])
    except getopt.GetoptError:
        usage()
        sys.exit(3)
    if not (options or args):
        usage()
        sys.exit(3)
    for opt, arg in options:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-t', '--title'):
            title = arg
        if opt in ('-v', '--verbose'):
            verbose = arg

    # verbose : ly01/mv and 6149 92A807ECDCBA00\nly01/mv ios 6149 BB3CD241AF8300\n
    # verbose : ly01/mv ios 6149 BB3CD241AF8300\n
    verbose = codecs.getdecoder("unicode_escape")(verbose)[0]
    return "%s \n %s" % (title, verbose)


#  一下开始判断
url = url_sign_robot()
try:
    data = run()
    data = pack_conent(data)
    r = requests.post(url, json=data,verify=False)
    print(r.text)
except Exception as e:
    print(e)

