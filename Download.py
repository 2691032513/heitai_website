import requests
from threading import Thread
from bs4 import BeautifulSoup
import xml
import os


def getMessages(crudePath):
    inform = dict()
    re = requests.get(crudePath)
    analyse = BeautifulSoup(re.content.decode('utf-8'), "lxml")
    inform['url:'] = crudePath
    inform["pageNum:"] = eval(analyse.find(id='tags').find_next_sibling().text[0:-6])
    inform["src:"] = analyse.find(id="thumbnail-container").img.attrs["src"]
    inform["src:"] = inform["src:"][:inform["src:"].rindex('/')] + "/full/"
    inform["title:"] = analyse.title.text.replace("|", " - ").replace("/", "-").replace(" ", "").replace("?",
                                                                                                         "").replace(
        ':', '-')
    inform["pictureFormat:"] = analyse.find(class_='lazyload')['src'][-4:]
    for tag in analyse.findAll('div', class_='tag-container field-name'):
        inform[next(tag.strings).replace('\n', '')] = [next(label.strings).replace('\n', '') for label in
                                                       tag.findAll(class_='tag tag-18024')]
    return inform


class Download(Thread):
    def __init__(self, url, example):
        super().__init__()
        self.info = getMessages(url)
        self.loadNum = 0
        self.example = example
        if not os.path.exists(self.info['title:']):
            os.mkdir(self.info['title:'])

    def run(self):
        if True:
            pass
        with open(self.info['title:'] + '\\' + 'readme.txt', 'w') as readme:
            for message in self.info.keys():
                readme.write(message + '  ' + self.info[message].__str__() + '\n')

        for index in range(self.info['pageNum:']):
            DownloadPicture(self, index + 1).start()

    def ignore(self):
        pass

if __name__ == '__main__':
    Download('https://hentaihand.com/comic/194169').start()


class DownloadPicture(Thread):
    def __init__(self, object, index):
        super().__init__()
        self.object = object
        self.index = index

    def run(self):
        pic = requests.get(self.object.info['src:'] + self.index.__str__() + self.object.info['pictureFormat:']).content
        with open(self.object.info['title:'] + '\\' + self.index.__str__() + self.object.info['pictureFormat:'],
                  'wb') as out:
            out.write(pic)
            self.object.loadNum += 1
            print(
                self.object.info['title:'] + ': complete   ' + self.object.loadNum.__str__() + ' / ' + self.object.info[
                    'pageNum:'].__str__())
