import requests
from bs4 import BeautifulSoup
import xml
import os
from Download import Download

if __name__ == '__main__':
    website = 'https://hentaihand.com/'
    url = 'https://hentaihand.com'
    example = dict()
    # prior : tags \ characters \parody
    example['prior'] = 'tags'
    example['isNew'] = 'yes'
    # 0 is main
    example['characters'] = [

    ]
    example['parody'] = [

    ]

    example['tags'] = [
        'full color'
    ]

    example['start'] = 2
    example['len'] = 1

    url += '/' + example['prior']
    url += '/' + (example[example['prior']][0]).replace(' ', '+')

    if example['isNew'] !='yes':
        url += '/' + 'popular?order='

    if url.find('?') == -1:
        url += '?page={}'
    else:
        url += '&page={}'

    taskList = list()

    for index in range(example['len']):
        print(url.format(example['start']+index))
        bs = BeautifulSoup(requests.get(url.format(example['start']+index)).content,'lxml')
        taskList.extend([result.find('a')['href'] for result in bs.findAll(class_='gallery')])

    for url in taskList:
        Download(website + url, example).start()


