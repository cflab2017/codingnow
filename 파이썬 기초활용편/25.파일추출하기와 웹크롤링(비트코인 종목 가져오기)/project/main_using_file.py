import pprint

def read_file(file_name):
    f = open(file_name, 'r', encoding='UTF8')
    while True:
        line = f.readline()
        if not line:
            break
        print(line)
    f.close()

# file_name = "./data/coinname_220503.html"
# read_file(file_name)

def read_file_and_parser(file_name):
    f = open(file_name, 'r', encoding='UTF8')
    lines = f.readlines()
    findLine = None
    find_krw = False
    coin_list = {}
    for line in lines:
        if not find_krw:
            if line.find('data-market="KRW"') >= 0:
                find_krw = True
            else:
                continue
        if line.find('tx_l tx_link') >= 0:
            findLine = ''

        if findLine is not None:
            findLine += line
            if findLine.find('</span>') >= 0:
                # findLine = findLine.replace('\n', '')
                print('1:',findLine)
                filter = ['\n', ' ', '"', '/KRW']
                for val in filter:
                    findLine = findLine.replace(val, '')
                print('2:', findLine)

                start = findLine.find('data-sorting=')+len('data-sorting=')
                end = findLine.find('</span>')
                findLine = findLine[start:end]
                findLine = findLine.split('>')
                coin_list[findLine[1]] = findLine[0]
                print('3:', findLine)
                print('----------------------------')
                findLine = None
                find_krw = False
    # print(coin_list)
    f.close()

    coin_list = sorted(coin_list.items())
    coin_list = dict(coin_list)
    pprint.pprint(coin_list, width=1)
    # print(coin_list)
    return coin_list

def write_to_file(coin_list, result_file_name):
    f = open(result_file_name, 'w', encoding='UTF8')
    f.write('coinlist = {\n')
    for key, data in coin_list.items():
        fdata = "'{}':'{}',\n".format(key, data)
        f.write(fdata)
    f.write('}\n')
    f.close()


file_name = "./data/coinname_220503.html"
coin_list = read_file_and_parser(file_name)

result_file_name = './result/coinlist_file.py'
write_to_file(coin_list,result_file_name)