from pixabay import Image
import random
import urllib.request


def find_image(search):
    API_KEY = '19162245-447c77f2e91a2fe67d8cd3dad'

    # image operations
    image = Image(API_KEY)

    # default image search
    img = image.search(search)

    hits = img['hits']

    i = 0
    for element in hits:
        i = i + 1
    # print(i)

    try:
        num = random.randint(0, i - 1)
        img = hits[num]
        url = img['largeImageURL']
    # print(url)
    except:
        url = ''
        pass
    return url


def download(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with open("img.jpg", "wb") as f:
        with urllib.request.urlopen(req) as r:
            f.write(r.read())
