from rich.console import Console
from rich import traceback
import argparse
import numpy.random as rand
import numpy as np
import numba
import time

console = Console()
console.clear()
traceback.install()

parser = argparse.ArgumentParser(description="Description")
parser.add_argument('-n_size', help='size of net', type=int, default=20)
parser.add_argument('-j', help='vale of parameter J', type=float, default='0.4')
parser.add_argument('-beta', help="value of parameter Beta", type=float, default='0.6')
parser.add_argument('-step', help='number of simulation steps', type=int, default='50')
parser.add_argument('-density', help="spin density", type=float, default='0.5')
parser.add_argument('-filename', help='name of file', type=str, default='step')
args = parser.parse_args()

console.print(f'[bold]Ising simulation : key parameters [/bold]')
console.print(f'Size of net : {args.n_size} \nParametr J : {args.j} \nParametr Beta : {args.beta}'
              f'\nSpin density : {args.density} \nNumber of simulation steps : {args.step}')
console.print(f'[bold]Start simulations : [/bold]\n')


def hamilton(field, j, beta):
    H = 0
    for i in range(field.shape[0]):
        for k in range(field.shape[1]):
            H = beta * field[(i, k)]
            if i > 0:
                H += j * field[(i, k)] * field[(i - 1, k)]
            if j > 0:
                H += j * field[(i, k)] * field[(i, k - 1)]
            if i < field.shape[0] - 1:
                H += j * field[(i, k)] * field[(i + 1, k)]
            if k < field.shape[1] - 1:
                H += j * field[(i, k)] * field[(i, k + 1)]
    return H


def without_numba(n_size, j, beta, step, density, field):
    for i in range(int(density * (n_size ** 2))):
        for x in range(n_size):
            for y in range(n_size):
                if rand.uniform(0, 1) < density:
                    field[(x, y)] = 1
                else:
                    field[(x, y)] = -1
    H0 = hamilton(field, j, beta)

    for step in range(step):
        for i in range(n_size ** 2):
            x = rand.randint(n_size)
            y = rand.randint(n_size)
            field[(x, y)] *= -1
            H1 = hamilton(field, j, beta)
            # field[(x, y)] *= -1
            if H1 - H0 < 0 or np.random.rand() < np.exp(-beta * (H1 - H0)):
                field[(x, y)] *= -1
                H0 = H1


@numba.jit(nopython=True)
def with_numba(n_size, j, beta, step, density, field):
    for i in range(int(density * (n_size ** 2))):
        for x in range(n_size):
            for y in range(n_size):
                if rand.uniform(0, 1) < density:
                    field[(x, y)] = 1
                else:
                    field[(x, y)] = -1
    H = 0

    for i in range(field.shape[0]):
        for k in range(field.shape[1]):
            H = beta * field[(i, k)]
            if i > 0:
                H += j * field[(i, k)] * field[(i - 1, k)]
            if j > 0:
                H += j * field[(i, k)] * field[(i, k - 1)]
            if i < field.shape[0] - 1:
                H += j * field[(i, k)] * field[(i + 1, k)]
            if k < field.shape[1] - 1:
                H += j * field[(i, k)] * field[(i, k + 1)]
    H0 = H
    for step in range(step):
        for i in range(n_size ** 2):
            x = rand.randint(n_size)
            y = rand.randint(n_size)
            field[(x, y)] *= -1
            for m in range(field.shape[0]):
                for k in range(field.shape[1]):
                    H = beta * field[(m, k)]
                    if m > 0:
                        H += j * field[(m, k)] * field[(m - 1, k)]
                    if k > 0:
                        H += j * field[(m, k)] * field[(m, k - 1)]
                    if m < field.shape[0] - 1:
                        H += j * field[(m, k)] * field[(m + 1, k)]
                    if k < field.shape[1] - 1:
                        H += j * field[(m, k)] * field[(m, k + 1)]
            H1 = H
            # field[(x, y)] *= -1
            if H1 - H0 < 0 or np.random.rand() < np.exp(-beta * (H1 - H0)):
                field[(x, y)] *= -1
                H0 = H1


class Simulation:
    def __init__(self, n_size, j, beta, step, density, filename):
        self.n_size = n_size
        self.field = np.ones((n_size, n_size), dtype=float, order='C')
        self.j = j
        self.beta = beta
        self.step = step
        self.density = density
        self.filename = filename
        t1 = time.time()
        without_numba(self.n_size, self.j, self.beta, self.step, self.density, self.field)
        t_without = time.time()
        self.field = np.ones((n_size, n_size), dtype=float, order='C')
        t2 = time.time()
        with_numba(self.n_size, self.j, self.beta, self.step, self.density, self.field)
        t_with = time.time()
        console.print(f'Simulation without numba: [bold]{t_without - t1}s [/bold]')
        console.print(f'\nSimulation with numba: [bold]{t_with - t2}s [/bold]')
        console.print(f'\nSimulation with numba is [bold]{(t_without - t1)/(t_with - t2)} [/bold] times better')


simulation = Simulation(n_size=args.n_size, j=args.j, beta=args.beta,
                        step=args.step, density=args.density, filename=args.filename)