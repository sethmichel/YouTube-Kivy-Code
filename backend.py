import datetime as dt
from math import sin         # plot handling
from random import uniform   # making fake ratings
from kivy_garden.graph import Graph, MeshLinePlot   # plot handling


# return tickers ratings for plot
def get_ratings():
    new_list = []
    holder = []

    # we don't have any ratings system, so just make some numbers
    for i in range(0, 5):
        for j in range(0, 10):
            holder.append(round(uniform(0, 10), 2))   # random rounded floats 0 - 10

        new_list.append(holder)
        holder = []

    return new_list



# will be the x-axis of plot. 10 most recent trading days
def make_dates():
    date_list = []

    date = dt.date.today()        # todays date
    week_index = date.weekday()   # mon = 0, sun = 6

    if (week_index > 4):                              # weekends are 5 or 6
        date -= dt.timedelta(days = week_index - 4)   # ex) sunday = 6. 6 - 4 = 2. 6 - 2 = fri

    # go backward from today (or fri if it's a weekend)
    for i in range(0, 10):
        # change weekends to fri
        if (date.weekday() == 6):
            date -= dt.timedelta(days = 2)

        date_list.insert(0, str(date.month) + "/" + str(date.day))

        date -= dt.timedelta(days = 1)

    return date_list



def make_plot(ratings_list, plot_dates, tickers_on_plot, plot_colors):
    # Prepare the data
    x = [1,2,3,4,5,6,7,8,9,10]
    plot = None

    # make the graph
    graph = Graph(ylabel='Ratings', x_ticks_major = 1, y_ticks_minor = 1, y_ticks_major = 1, 
                  y_grid_label=True, x_grid_label=False, padding=5, x_grid=True, y_grid=True, 
                  xmin=0, xmax=10, ymin=0, ymax=10)

    if (len(tickers_on_plot) > 0):
        for i in range(0, len(tickers_on_plot)):
            plot = MeshLinePlot(color = plot_colors[i])
            
            plot.points = [(i, j) for i, j in zip(x, ratings_list[i])]

            graph.add_plot(plot)

    return graph














