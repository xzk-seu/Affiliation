from Logger import logger


proxy_list = [
    {
        "proxyHost": "http-proxy-sg2.dobel.cn",
        "proxyPort": "9180",
        "proxyUser": "ZYYTHTT1",
        "proxyPass": "6tEQ26bA9"
    },
    {
        "proxyHost": "http-dyn.abuyun.com",
        "proxyPort": "9020",
        "proxyUser": "HE67H8188DLDT85D",
        "proxyPass": "4145553046D4B3BB"
    },
    {
        "proxyHost": "http-dyn.abuyun.com",
        "proxyPort": "9020",
        "proxyUser": "H8461Q488M583V1D",
        "proxyPass": "D90F780427E4D69E"
    },
    {
        "proxyHost": "http-dyn.abuyun.com",
        "proxyPort": "9020",
        "proxyUser": "HX5596WE9Q2XJ4D",
        "proxyPass": "21F210078BAEA359"
    },
    {
        "proxyHost": "http-dyn.abuyun.com",
        "proxyPort": "9020",
        "proxyUser": "HX0N9NRC2F5394LD",
        "proxyPass": "74E67958CBF14561"
    },
    {
        "proxyHost": "http-proxy-sg2.dobel.cn",
        "proxyPort": "9180",
        "proxyUser": "DONGNANHTT1",
        "proxyPass": "T74B13bQ"
    },
    {
        "proxyHost": "proxy.crawlera.com",
        "proxyPort": "8010",
        "proxyAuth": "78d4b6f49900465f881f63b4b1de4029"
    }
]


def proxy_cfg():
    proxy_id = int(input('input proxy id: '))
    r_proxy = None
    if proxy_id in range(len(proxy_list)):
        proxy_info = proxy_list[proxy_id]
        proxyHost = proxy_info['proxyHost']
        if proxyHost == "proxy.crawlera.com":
            proxyPort = proxy_info['proxyPort']
            proxyAuth = proxy_info['proxyAuth']
            logger.info('proxy: %s is chosen!\n' % proxyHost)
            r_proxy = {"https": "https://{}@{}:{}/".format(proxyAuth, proxyHost, proxyPort),
                       "http": "http://{}@{}:{}/".format(proxyAuth, proxyHost, proxyPort)}
            return r_proxy
        proxyPort = proxy_info['proxyPort']
        proxyUser = proxy_info['proxyUser']
        proxyPass = proxy_info['proxyPass']
        logger.info('proxy: %s is chosen!\n' % proxyUser)
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        r_proxy = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
    else:
        logger.info('proxy is None!')
    return r_proxy


