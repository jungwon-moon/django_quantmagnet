import requests
from bs4 import BeautifulSoup as bs


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}


def get_kr_base_rate():
    r"""
    한국은행 기준금리 추이
    """
    url = f"https://www.bok.or.kr/portal/singl/baseRate/list.do?dataSeCd=01&menuNo=200643"
    r = requests.get(url, headers=headers)
    soup = bs(r.text, 'html.parser')
    data = soup.find('tbody').find_all('td')
    results = []

    for i in range((len(data)+1)//3):
        year = data[i*3].getText()
        mmdd = ''.join(map(lambda x: x[:2], data[i*3+1].getText().split(' ')))
        rate = data[i*3+2].getText()
        results.append([''.join([year, mmdd]), rate])

    return results
