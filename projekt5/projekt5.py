# terminal : jupyter-lab
# pozniej terminal : bokeh serve ./projekt5_.py --show

import numpy as np
import pandas as pd
from bokeh.io import output_notebook, curdoc
from bokeh.layouts import column, row
from bokeh.models import Label
from bokeh.palettes import Set3
from bokeh.plotting import figure
from bokeh.transform import cumsum

output_notebook()
################################# DANE #################
dogs = {
    'United States': 70,
    'Brazil': 35.8,
    'China': 27.4,
    'Russia': 12.5,
    'Japan': 12,
    'Phillipines': 11.6,
    'India': 10.2,
    'Argentina': 9.2,
    'United Kingdom': 9,
    'France': 7.4,
}
x = np.linspace(-20 * np.pi, 20 * np.pi, 5000)
y_sin = np.sin(x)
y_cos = np.cos(x)
data_sin = {'x': x, 'y_sin': y_sin, 'y_cos': y_cos}
################################# WYKRES I #################
data = pd.Series(dogs).reset_index(name='value').rename(columns={'index': 'country'})
data['angle'] = data['value'] / data['value'].sum() * 2 * 3.14
data['color'] = Set3[len(dogs)]

fig1 = figure(width=800, title="Countries with the most dogs wordwide (milion)", tools="hover",
              tooltips="@country: @value", x_range=(-0.5, 1.0))

fig1.wedge(x=0, y=1, radius=0.4,
           start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
           line_color="white", fill_color='color', legend_field='country', source=data)
label = Label(x=400, y=80, x_units='screen', y_units='screen',
              text='in Poland we have 7.3 M', render_mode='css',
              border_line_color='pink', border_line_alpha=1.0,
              background_fill_color='white', background_fill_alpha=1.0)
fig1.add_layout(label)
fig1.axis.axis_label = None
fig1.axis.visible = False
fig1.grid.grid_line_color = None
# show(fig1)

################################# WYKRES II #################
fig2 = figure(title="Sinus", x_axis_label='x', y_axis_label='y', x_range=(-np.pi, np.pi))
fig2.circle(x, y_sin)
fig2.line(x, y_sin, color='red')
# show(fig2)

################################# WYKRES III #################
dogs_list = [(country_name, numer_dogs) for country_name, numer_dogs in dogs.items()]
dogs_array = np.asarray(dogs_list)
dogs_t1, dogs_t2 = [], []
for c_name in range(len(dogs_array)):
    dogs_t1.append(dogs_array[c_name][0])
    dogs_t2.append(dogs_array[c_name][1])

fig3 = figure(title="Countries with the most dogs wordwide (milion)", y_range=dogs_t1, x_range=[0, 80], width=600,
              height=800)
fig3.segment(x0=0, y0=dogs_t1, x1=dogs_t2, y1=dogs_t1, line_color="#f4a582", line_width=4)
fig3.circle(x=dogs_t2, y=dogs_t1, size=8, line_color="#f4a582", fill_color="white", line_width=4)
# show(fig3)

################################# WYKRES IV #################
fig4 = figure(x_range=dogs_t1, title="Countries with the most dogs wordwide (milion)", width=600, height=800)
fig4.vbar(x=dogs_t1, top=dogs_t2, width=0.5, line_color="black", fill_color="#f4a582")
fig4.y_range.start = 0
# show(fig4)


l1 = column([fig2, fig1], sizing_mode='fixed')
# l3 = column([fig1],)
l2 = row([fig3, fig4], sizing_mode="fixed")

layout = column(l1, l2)
curdoc().add_root(layout)
curdoc().title = "Iga's word"
