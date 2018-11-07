import json


if __name__ == '__main__':
    with open('affiliation_lo_la.json', 'r') as fr:
        js = json.load(fr)
    print(len(js))
    r_dict = dict()
    for k, v in js.items():
        if v['lo'] == 0:
            print(k, v)
        else:
            r_dict[k] = v
    print(len(r_dict))
    with open('lola.json', 'w') as fw:
        json.dump(r_dict, fw)
