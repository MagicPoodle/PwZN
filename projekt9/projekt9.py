import requests

from rich.console import Console
from rich import traceback
import aiohttp
import asyncio
import time

console = Console()
console.clear()
traceback.install()
url = 'https://jsonplaceholder.typicode.com/todos/'
data = 20
colour = 'red'


def classic():
    for number in range(1,data+1):
        web = requests.get(url + str(number))
        web_D = web.json()
        console.print(f"[{colour}]{number}. [/{colour}]{web_D} \n")


async def main():
    async with aiohttp.ClientSession() as session:
        for number in range(1,data+1):
            async with session.get(url + str(number)) as response:
                webA_D = await response.json()
                console.print(f"[{colour}]{number}.[/{colour}] {webA_D}\n")


console.print(f"[bold][{colour}]Pobierania naglowkow ze strony : {url}[/{colour}][/bold]\n")
console.print("[bold]Rozpoczacie klasycznego pobierania[/bold]")
t1 = time.time()
classic()
t2 = time.time()
console.print("[bold]Koniec klasycznego pobierania. \nRoczoczecie asynchronicznego pobierania.[/bold]")
t3 = time.time()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
t4 = time.time()
console.print("[bold]Koniec asynchronicznego pobierania.[/bold]")
console.print(f"\nKlasyczne pobieranie zajelo : {t2 - t1} sekund")
console.print(f"Asynchroniczne pobieranie zajelo : {t4 - t3} sekund")
