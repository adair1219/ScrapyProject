import requests
import re

def get_cate(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            get_cate(url)
    except:
        pass

def parse_cateid(response):
    _cateid = re.findall('cateID\:(.*?)\,', response.text, re.S)
    _catelist = re.findall('listName\:"(.*?)"\,', response.text, re.S)
    result_dict = dict(zip(_catelist, _cateid))
    return result_dict

def save_tO_local(result):
    with open('cateid.py', 'a', encoding='utf-8') as f:
        f.write(str(result))

if __name__ == '__main__':
    url = 'https://j1.58cdn.com.cn/job/pc/full/cate/0.1/jobCates.js?v=0'
    response = get_cate(url)
    result = parse_cateid(response)
    save_tO_local(result)