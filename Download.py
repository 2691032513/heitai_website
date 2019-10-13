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
    inform["small:"] = analyse.find(class_='gallerythumb').find('img')['src']
    inform["small:"] = inform['small:'][:inform['small:'].rindex('/')] + inform['small:'][inform['small:'].rindex('/'):].replace('1','{}')
    inform["title:"] = analyse.title.text.replace("|", " - ").replace("/", "-").replace(" ", "").replace("?",
                                                                                                         "").replace(
        ':', '-')
    inform["pictureFormat:"] = analyse.find(class_='lazyload')['src'][-4:]
    inform['routes'] = [
        inform['src:'] + '{}' + inform["pictureFormat:"],
        inform['src:'] + '{}' + '.png' if inform["pictureFormat:"] == '.jpg' else '.jpg',
        inform["small:"],
        inform["small:"].replace(inform["small:"][-4:], '.png' if inform["small:"][-4:] == '.jpg' else '.jpg')
    ]

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

    def run(self):
        if self.isIgnored():
            print('ignored: ' + self.info['title:'])
            return

        if not os.path.exists(self.info['title:']):
            os.mkdir(self.info['title:'])

        with open(self.info['title:'] + '/' + 'readme.txt', 'w') as readme:
            for message in self.info.keys():
                if message == 'routes':
                    continue
                readme.write(message + '  ' + self.info[message].__str__() + '\n\n')

        for index in range(self.info['pageNum:']):
            DownloadPicture(self, index + 1).start()

    def isIgnored(self):
        for t in self.example['tags']:
            if t not in self.info['Tags:']:
                return True


if __name__ == '__main__':
    Download('https://hentaihand.com/comic/195024/c94-house-saibai-mochi-sh',
             {
                 'tags': [
                     'lolicon'
                 ]
             }).start()


class DownloadPicture(Thread):
    def __init__(self, object, index):
        super().__init__()
        self.object = object
        self.index = index

    def run(self):
        path = './' + self.object.info['title:'] + '/' + self.index.__str__() + self.object.info['pictureFormat:']
        for url in self.object.info['routes']:
            pic = requests.get(url.format(self.index)).content
            with open(path, 'wb') as out:
                out.write(pic)
                out.close()
                if os.path.getsize(path) <= 2048:
                    os.remove(path)
                else:
                    break
        self.object.loadNum += 1
        picSize = os.path.getsize(path)//1024 if os.path.exists(path) else 'None'
        print(self.object.info['title:'] + ':\n complete:   ' + self.object.loadNum.__str__() + ' / ' + self.object.info['pageNum:'].__str__() + '    page:' + self.index.__str__() + '   size: ' + picSize.__str__() + '\n')
