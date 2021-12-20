from rich.console import Console
import rich.traceback
from timeit import default_timer as timer
from time import sleep
import numpy as np
import functools

console = Console()
console.clear()
rich.traceback.install()

diff_time = []


def check_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'n' in kwargs:
            for replay in range(kwargs.get('n')):
                start = timer()
                func(*args, **kwargs)
                end = timer()
                diff_time.append(end - start)
            colour = 'red'
            console.log(f"[{colour}]The number of executions : [/{colour}]{kwargs.get('n')}")
            console.log(f'[{colour}]Time of one execution : [/{colour}]{diff_time} s')
            console.log(f'[{colour}]Mean time of all executions : [/{colour}]{np.mean(diff_time)} s')
        else:
            start = timer()
            func(*args, **kwargs)
            end = timer()
            diff_time.append(end - start)
            console.log(f'Time of one execution : {diff_time} s')
        # return func(*args, **kwargs)

    return wrapper


@check_time
def function(**kwargs):
    sleep(np.random.randint(0, 2))
    console.print("Nice decorator")


function(n=10)
# function()
