import requests
import re
from bs4 import BeautifulSoup
from rich.console import Console
from rich import traceback
import time
from concurrent.futures import ProcessPoolExecutor
from PIL import Image

console = Console()
console.clear()
traceback.install()
url = "http://www.if.pw.edu.pl/~mrow/dyd/wdprir/"


def dowland(name):
    file = open(name, "wb")
    src = url + name
    console.print(src)
    file.write(requests.get(src).content)
    file.close()
    picture = Image.open(name)
    picture = picture.convert('L')
    picture.save(name)


if __name__ == '__main__':
    web = requests.get('http://www.if.pw.edu.pl/~mrow/dyd/wdprir/')
    soup = BeautifulSoup(web.text, 'html.parser')
    console.print(f'Website name : {soup.title.text}')
    picture_links = soup.find_all('a', href=re.compile('png'))
    picture_href = [img['href'] for img in picture_links]

    pool = ProcessPoolExecutor(12)
    console.print("Start's downloading ...")
    start = time.time()
    for names in range(len(picture_href)):
        console.print(f'{names + 1}. {picture_href[names]}')
        fs = [pool.submit(dowland, picture_href[names])]
        rs = [f.result() for f in fs]
    end = time.time()
    console.print(f'\nEnd.\nDownload and change time: {end - start}')