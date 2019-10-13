import os

import requests
from threading import Thread
from bs4 import BeautifulSoup

global counter

counter = 0
global max


class DownLoad(Thread):
    global counter, max

    def __init__(self, linkUrl, index):
        super().__init__()
        self.url = linkUrl
        self.index = index

    def run(self):
        global counter, max
        con = requests.get(self.url).content
        with open(self.index.__str__() + message["pictureFormat:"], "wb") as out:
            out.write(con)
            out.close()
            counter = counter + 1
            print("download page " + self.index.__str__() + " finish   -------  " + counter.__str__() + " / " + max.__str__())


def getMessages(crudePath):
    inform = dict()
    re = requests.get(crudePath)
    analyse = BeautifulSoup(re.content.decode('utf-8'), "lxml")
    inform['url:'] = crudePath
    inform["pageNum:"] = eval(analyse.find(id='tags').find_next_sibling().text[0:-6])
    inform["src:"] = analyse.find(id="thumbnail-container").img.attrs["src"]
    inform["src:"] = inform["src:"][:inform["src:"].rindex('/')] + "/full/"
    inform["title:"] = analyse.title.text.replace("|", " - ").replace("/", "-").replace(" ", "").replace("?", "")
    inform["pictureFormat:"] = analyse.find(class_='lazyload')['src'][-4:]
    for tag in analyse.findAll('div', class_='tag-container field-name'):
        inform[next(tag.strings).replace('\n', '')] =[next(label.strings).replace('\n','') for label in tag.findAll(class_='tag tag-18024')]
    return inform


if __name__ == '__main__':
    message = getMessages(input("please input your url:  "))
    boole = input()
    if not os.path.exists(message["title:"]):
        os.mkdir(message["title:"])
    os.chdir(message["title:"])
    max = message["pageNum:"]
    if boole.__eq__("error"):
        max //= 2
    print(message)

    with open('./readme.txt', 'w') as readme:
        for mes in message.keys():
            readme.write(mes.__str__() + ' ' + message[mes].__str__() + '\n')
    print("\n---------------------------------------- task start ---------------------------------------------\n")
    for i in range(1, max + 1):
        url = message["src:"] + i.__str__() + message['pictureFormat:'].__str__()
        DownLoad(url, i).start()
