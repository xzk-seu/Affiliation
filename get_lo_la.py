import os
import json


def get_lo_la():
    r_dict = dict()
    path = os.path.join(os.getcwd(), 'affiliation_data')
    file_list = os.listdir(path)
    for file in file_list:
        print(file)
        file_name = os.path.join(path, file)
        with open(file_name, 'r') as fr:
            js = json.load(fr)
        a_id = js['id']
        data = js['data']
        if not data:
            print(a_id, js['name'])
            continue
        entity = js['data']['entity']
        lo = entity.setdefault('lo', 0)
        la = entity.setdefault('la', 0)
        r_dict[a_id] = {'name': js['name'],
                        'lo': lo,
                        'la': la}
    with open('affiliation_lo_la.json', 'w') as fw:
        json.dump(r_dict, fw)


if __name__ == '__main__':
    get_lo_la()
