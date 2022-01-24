import pandas as pd
from rich.console import Console
from rich import traceback
import matplotlib.pyplot as plt

console = Console()
console.clear()
traceback.install()
colour = 'red'
films = pd.read_csv('films_10', sep=';', encoding="ISO-8859-1", skiprows=[1],
                    dtype={'Length': 'float64', 'Popularity': 'float64'},
                    usecols=['Year', 'Length', 'Title', 'Subject'])

GroupS = films.groupby('Subject')
console.print(f"[{colour}]Podzial fimow ze wzgledu na rodzaj:[/{colour}]\n{GroupS.count()}")
console.print(f"\n[{colour}]Srednia dlugosc filmow roznych rodzajow:[/{colour}] \n{GroupS.Length.mean()}")
console.print(
    f"\n[{colour}]Maksymalna i minimalna dlugosc filmow:[/{colour}] \n{GroupS.agg({'Length': ['min', 'max']})}")

likes = pd.DataFrame({'Subject': ['Action', 'Adventure', 'Comedy', 'Crime', 'Horror', 'Music', 'Mystery', 'Romance',
                                  'Science Fiction', 'Short', 'War', 'Western', 'Drama', 'Fantasy'],
                      'Like': ['Yes', 'Yes', 'Yes', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'Yes',
                               'Yes']})

F_L = pd.merge(films, likes, on='Subject', how='outer')
films_likes = F_L.groupby(["Like", "Subject"])
console.print(f"\n[{colour}]Podzial na fimy i rodzaje jakie lubie i nie lubie:[/{colour}] "
              f"\n{films_likes.count()}")

minmaxplot = pd.read_csv('minmax.csv')
minmaxplot.plot("Subject", ["min", "max"], marker='o')
plt.ylabel("Min i max czas trwania")
plt.show()
