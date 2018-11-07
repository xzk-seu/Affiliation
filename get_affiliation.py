import requests
import json
import random
from Logger import logger
import time
import os
from multiprocessing import Pool
from proxy import proxy_cfg


_HOST = 'https://academic.microsoft.com/api/browse/GetEntityDetails'
_SESSION = requests.session()
_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'academic.microsoft.com',
    'Cookie': 'msacademic=25bcc582-e762-4073-a219-2742783e18cc; ai_user=iGCCu|2018-08-21T03:48:49.213Z; MC1=GUID=865157eb0f744a43b5c84d940f20405c' + str(random.randint(100,200)) + '&HASH=8651&LV=201809&V=4&LU=1536480320543; AMCV_EA76ADE95776D2EC7F000101%40AdobeOrg=-894706358%7CMCIDTS%7C17800%7CMCMID%7C29525519319229170001339901827044472388%7CMCAAMLH-1538483649%7C11%7CMCAAMB-1538483649%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCCIDH%7C-629512180%7CMCOPTOUT-1537886049s%7CNONE%7CvVersion%7C2.3.0; aamoptsegs=aam%3Dtest; MUID=3CD3DE2F3E4762BF3FB5D2063A4761D8; ARRAffinity=8463499082e39d2b88debe78834cc4844d3316c54a3bab90504386ef74fc71c3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
}
_MAXRETRY = 6
_ERRORMESSAGE = "id: {0} | Error: {1}"
_INFOMESSAGE = "id: {0} has done."


def _get_request(url, param=None, proxies=None):
    resp = _SESSION.get(
        url,
        params=param,
        headers=_HEADERS,
        proxies=proxies,
        # verify=False,
        timeout=random.choice(range(30, 100))
    )
    resp.encoding = "utf-8"
    if resp.status_code == 200:
        return resp.text
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


def get_data(entity_id, proxies):
    tries = 0
    js = dict()
    param = {'entityId': entity_id}
    while tries < _MAXRETRY:
        tries += 1
        try:
            html = _get_request(_HOST, param, proxies)
            js = json.loads(html.strip())
            break
        except Exception as e:
            if tries < _MAXRETRY:
                logger.info(_ERRORMESSAGE.format(str(entity_id), str(e)) + " | tries: %d" % tries)
            else:
                logger.error(_ERRORMESSAGE.format(str(entity_id), str(e)) + " | tries: %d" % tries)
            time.sleep(tries)
    return js


def write_data_proc(a_id, a_name, proxies):
    r = get_data(a_id, proxies)
    res_dict = {'id': a_id,
                'name': a_name,
                'data': r}
    path = os.path.join(os.getcwd(), 'affiliation_data')
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = os.path.join(path, '%s.json' % a_id)
    with open(file_name, 'w') as fw:
        json.dump(res_dict, fw)
        logger.info("id: %s\t name: %s" % (str(a_id), res_dict["name"]))


def get_affiliation_list(file_name):
    with open(file_name, 'r') as fr:
        js = json.load(fr)
    return js


def get_remain(total_list):
    path = os.path.join(os.getcwd(), 'affiliation_data')
    if not os.path.exists(path):
        os.makedirs(path)
    file_list = os.listdir(path)
    existing = set()
    for file in file_list:
        existing.add(file.split('.')[0])

    remain = dict()
    for k, v in total_list.items():
        if k not in existing:
            remain[k] = v

    # remain = set(total_list) - existing
    logger.info('all task: %d' % len(total_list))
    logger.info('existing: %d' % len(existing))
    logger.info('remain: %d' % len(remain))
    return remain


if __name__ == '__main__':
    # 使用时改写get_author_list()函数
    pool = Pool(8)
    prox = proxy_cfg()
    # t_id = int(input('please input task id: '))
    # a_list = get_author_list(t_id)
    a_list = get_affiliation_list('med_affiliations.json')
    a_list = get_remain(a_list)
    for affiliation_id, affiliation_name in a_list.items():
        pool.apply_async(write_data_proc, (affiliation_id, affiliation_name, prox))
    pool.close()
    pool.join()


