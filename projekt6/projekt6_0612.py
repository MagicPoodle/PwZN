from rich.console import Console
import rich.traceback
from timeit import default_timer as timer
import numpy as np
import functools

console = Console()
console.clear()
rich.traceback.install()

diff_time = []


def decorator(a=1):
    def check_time(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for replay in range(a):
                start = timer()
                func(*args, **kwargs)
                end = timer()
                diff_time.append(end-start)
            colour = 'red'
            console.log(f"[{colour}]\nThe number of elements : [/{colour}]{a}")
            console.log(f'[{colour}]Time of one execution : [/{colour}]{diff_time} s')
            console.log(f'[{colour}]Mean time of all executions : [/{colour}]{np.mean(diff_time)} s')

        return wrapper
    return check_time


def function(*args):
    n = args[0]
    b = np.random.randint(n, n*2)
    x = np.linspace(1, b * 2, n)
    y = np.linspace(1, b*3, n)
    calculate = x*y/np.pi
    return console.print(f'[bold]Result :[/bold] \n {calculate}')

decorator()(function)(8)
#decorator(4)(function)(8)
