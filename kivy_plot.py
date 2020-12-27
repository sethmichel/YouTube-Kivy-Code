from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView

import backend

# all graphics/widgets: grids, btns, labels for all data
class Main_Page(BoxLayout):
    def __init__(self, **kwargs):
        super(Main_Page, self).__init__(**kwargs)      # this is only for if kivy code goes in the py file



        self.orientation = 'horizontal'

        bad_graph_btn = Button(text = "bad graph")
        bad_graph_btn.bind(on_release = self.bad_handle_plot)

        good_graph_btn = Button(text = "good graph")
        good_graph_btn.bind(on_release = self.good_handle_plot)

        self.add_widget(bad_graph_btn)
        self.add_widget(good_graph_btn)






        self.ticker_list = ['pays', 'pi', 'amd', 'cde', 'x', "msft"]

        # tickers to show on the plot
        self.tickers_on_plot = ['pays']

        # red, yellow, purple, light blue, green | line colors for plot
        self.plot_colors = [[1,1,0,1], [1,0,0,1], [1,0,1,1], [0.5,.75,.9,1], [0,1,0.3,1]]
        
        # holds ratings for the plot
        self.plot_ratings = backend.get_ratings()

        # x-axis of plot, 10 most recent trading dates
        self.plot_dates = backend.make_dates()




    def bad_handle_plot(self, instance):
        view = ModalView(size_hint = (0.75, 0.75))

        graph =  backend.make_plot(self.plot_ratings, self.plot_dates, self.tickers_on_plot, self.plot_colors)

        view.add_widget(graph)
        view.open()



    # I have a ticker list with a bunch of tickers, and a tickers_on_plot list that will change
    # depending on what I click to plot. So ticker_list vs tickers_on_plot
    def good_handle_plot(self, instance):
        mainview = ModalView(size_hint = (0.75, 0.75))
        box = BoxLayout(orientation = "horizontal", padding = [0,15,15,10])   # left, top, right, bot

        # make a the left side (will contain a 2 other layouts)
        leftbox = BoxLayout(orientation = "vertical", size_hint_x = 0.3)

        # will contain the ticker gridlayout (top left)
        scroll = ScrollView(do_scroll_x = False, do_scroll_y = True)

        # holds tickers (top left that will be scrollable)
        ticker_grid = GridLayout(rows = len(self.ticker_list), cols = 2, size_hint_y = None)
        
        # makes the gridlayout scrollabel (top left)
        ticker_grid.bind(minimum_height = ticker_grid.setter("height"))

        # populate the top left scrollable gridlayout (area that shows what tickers are shown)
        # will be marked X or + depending on if it's being shown
        for i in range(0, len(self.ticker_list)):
            ticker_grid.add_widget(Label(text = self.ticker_list[i], size_hint_x = 0.6))
            ticker_grid.add_widget(Button(text = "+", size_hint_x = 0.4))

            # if ticker is shown on plot
            if ((self.ticker_list[i] in self.tickers_on_plot) and len(self.tickers_on_plot) > 0):
                ticker_grid.children[0].text = 'X'
                ticker_grid.children[0].background_color = [1,0,0,1]

            # bind event methods to btns
            if (ticker_grid.children[0].text == "+"):
                ticker_grid.children[0].fbind("on_release", self.plot_add_ticker, ticker_grid.children[1].text, mainview)
            else:
                ticker_grid.children[0].fbind("on_release", self.plot_cancel_ticker, ticker_grid.children[1].text, mainview)

        # right side that will be graph - recall I make my own x-axis
        rightbox = BoxLayout(orientation = "vertical")

        # x-axis for graph (right side of modalview)
        rightbotgrid = GridLayout(rows = 1, cols = 13, size_hint_y = 0.05)

        # make invisible labels for formatting
        # this is an invsible widget just to make things fit
        rightbotgrid.add_widget(Label(size_hint_x = 1/13))
        for i in range(1, 10):
            # make actual labels - 1/13 is just what fit
            rightbotgrid.add_widget(Label(text = self.plot_dates[i], size_hint_x = 1/13))

        # combine everything
        scroll.add_widget(ticker_grid)
        leftbox.add_widget(scroll)
        
        # the graph doesn't have legend functionality, so make one
        leftbox.add_widget(self.plot_make_legend())
        
        # make the actual plot
        rightbox.add_widget(backend.make_plot(self.plot_ratings, self.plot_dates, self.tickers_on_plot, self.plot_colors))
        
        # add the x-axis
        rightbox.add_widget(rightbotgrid)
        rightbox.add_widget(Label(text = "Dates", size_hint_y = 0.05))
        
        box.add_widget(leftbox)
        box.add_widget(rightbox)
        mainview.add_widget(box)

        mainview.open()
        


    # makes a legend (key)
    def plot_make_legend(self):
        # containg_box is just the label saying "legend" then the actual legend
        containing_box = BoxLayout(orientation = "vertical", size_hint_y = 0.5, padding = 10)
        containing_box.add_widget(Label(text = "Legend", size_hint = (1, 0.1)))

        # this is the actual legend
        legend_grid = GridLayout(rows = 6, cols = 2)
        legend_grid.add_widget(Label(text = "Ticker"))   # col title
        legend_grid.add_widget(Label(text = "Color"))    # col title
        
        # populated legend_grid
        for i in range(0, len(self.tickers_on_plot)):
            legend_grid.add_widget(Label(text = self.tickers_on_plot[i]))
            legend_grid.add_widget(Button(background_color = self.plot_colors[i], disabled = True, background_disabled_normal = ""))

        for i in range(len(legend_grid.children) - 1, 11):
            legend_grid.add_widget(Label())

        containing_box.add_widget(legend_grid)

        return containing_box



    # EVENT: user clicked btn to cancel a ticker from the modalview - so erase it
    # pm: ticker = 'cde', instance = X btn clicked
    def plot_cancel_ticker(self, ticker, mainview, instance):
        spot = self.tickers_on_plot.index(ticker)
        instance.text = "+"
        instance.background_color = [1, 1, 1, 1]
        
        del self.tickers_on_plot[spot]

        mainview.dismiss()            # cancel modalview
        self.good_handle_plot(None)   # restart modalview, none replaces instance


    # pm: ticker = 'cde', instance = + btn clicked
    def plot_add_ticker(self, ticker, mainview, instance):
        if (len(self.tickers_on_plot) == 5):
            return

        instance.text = "X"
        instance.background_color = [1,0,0,1]
        
        self.tickers_on_plot.append(ticker)

        mainview.dismiss()            # cancel modalview
        self.good_handle_plot(None)   # restart modalview, none replaces instance

        













class myApp(App):
    def build(self):
        return Main_Page()

if __name__ == "__main__":
    myApp().run()





