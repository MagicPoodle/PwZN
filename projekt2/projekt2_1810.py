from rich.console import Console
from rich import traceback
from PIL import Image
from rich.progress import track
import argparse
import numpy.random as rand
import numpy as np

console = Console()
console.clear()
traceback.install()

parser = argparse.ArgumentParser(description="Description")
parser.add_argument('-n_size', help='size of net', type=int, default=20)
parser.add_argument('-j', help='vale of parameter J', type=float, default='0.4')
parser.add_argument('-beta', help="value of parameter Beta", type=float, default='0.6')
parser.add_argument('--h', help="value of magnetic field H", type=float, default='0.5')
parser.add_argument('-step', help='number of simulation steps', type=int, default='50')
parser.add_argument('-density', help="spin density", type=float, default='0.5')
parser.add_argument('-filename', help='name of file', type=str, default='step')
args = parser.parse_args()

console.print(f'[bold]Ising simulation : key parameters [/bold]')
console.print(f'Size of net : {args.n_size} \nParametr J : {args.j} \nParametr Beta : {args.beta}'
              f'\nSpin density : {args.density} \nNumber of simulation steps : {args.step}')


class Simulation():
    def __init__(self, n_size, j, beta, step, density, filename):
        self.n_size = n_size
        self.field = np.ones((n_size, n_size), dtype=float, order='C')
        self.j = j
        self.beta = beta
        self.step = step
        self.density = density
        self.filename = filename
        self.image = []
        for i in range(int(self.density * (self.n_size ** 2))):
            for x in range(self.n_size):
                for y in range(self.n_size):
                    if rand.uniform(0, 1) < self.density:
                        self.field[(x, y)] = 1
                    else:
                        self.field[(x, y)] = -1
        H0 = self.hamilton()
        console.print(f'[bold]Start simulation : [/bold]\n')

        for step in track(range(self.step)):
            for i in range(self.n_size ** 2):
                x = rand.randint(self.n_size)
                y = rand.randint(self.n_size)
                self.field[(x, y)] *= -1
                H1 = self.hamilton()
                # self.field[(x, y)] *= -1
                if H1 - H0 < 0 or np.random.rand() < np.exp(-self.beta * (H1 - H0)):
                    self.field[(x, y)] *= -1
                    H0 = H1

            picture = np.zeros((self.n_size*10, self.n_size*10))
            for i in range(self.n_size):
                for j in range(self.n_size):
                    if self.field[(i, j)] == 1:
                        for k in range(10):
                            for l in range(10):
                                picture[(i*10+k, j*10+l)] = 123

            image = Image.fromarray(picture)
            image = image.convert('RGB')
            self.image.append(image)
            imagepath = "Obrazki/"
            image.save(f"{imagepath}" + self.filename + str(step + 1) + ".jpg")
        console.print(f'\n[bold]End simulation.[/bold]')

    def hamilton(self):
        H = 0
        for i in range(self.field.shape[0]):
            for j in range(self.field.shape[1]):
                H = self.beta * self.field[(i, j)]
                if i > 0:
                    H += self.j * self.field[(i, j)] * self.field[(i - 1, j)]
                if j > 0:
                    H += self.j * self.field[(i, j)] * self.field[(i, j - 1)]
                if i < self.field.shape[0] - 1:
                    H += self.j * self.field[(i, j)] * self.field[(i + 1, j)]
                if j < self.field.shape[1] - 1:
                    H += self.j * self.field[(i, j)] * self.field[(i, j + 1)]
        return H


simulation = Simulation(n_size=args.n_size, j=args.j, beta=args.beta,
                        step=args.step, density=args.density, filename=args.filename)