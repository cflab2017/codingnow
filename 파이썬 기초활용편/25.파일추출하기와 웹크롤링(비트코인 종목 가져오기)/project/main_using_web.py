from bs4 import BeautifulSoup as bs4
import requests
import pprint
#pip install requests
#pip install bs4

def get_coinlist_from_web(URL):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    rq = requests.get(URL,headers=header)
    soup = bs4(rq.content, 'html.parser')

    # li_list = soup.find_all('li', class_='fvtWrap')
    li_list = soup.find_all(
                'li', 
                {'class': 'fvtWrap', 'data-market': 'KRW', 'data-fixed': 'N'}
            )
    coin_list = {}
    for li in li_list:
        # if ('data-market' in li.attrs.keys()) and li.attrs['data-market'] == "KRW":
        se = li.select('span')
        # print(se)
        coin = se[0].text.replace('/KRW', '')
        name = se[0].attrs['data-sorting']
        coin_list[coin] = name
        # print(coin, name)

    coin_list = sorted(coin_list.items())
    coin_list = dict(coin_list)
    pprint.pprint(coin_list, width=1)
    return coin_list

def write_to_file(coin_list, result_file_name):
    f = open(result_file_name, 'w', encoding='UTF8')
    f.write('coinlist = {\n')
    for key, data in coin_list.items():
        fdata = "'{}':'{}',\n".format(key, data)
        f.write(fdata)
    f.write('}\n')
    f.close()

url = 'https://www.bithumb.com/trade/order/BTC_KRW'
coin_list = get_coinlist_from_web(url)

result_file_name = './result/coinlist_web.py'
write_to_file(coin_list, result_file_name)

