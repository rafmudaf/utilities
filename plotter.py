#!/usr/local/bin/python3

import matplotlib.pyplot as plt

class Plot():
    def __init__(self, title, xchannel, xunits, xdata):
        plt.figure()
        self.title = title
        self.xchannel = xchannel
        self.xunits = xunits
        self.xdata = xdata
        self.fontsize = 14

    def _configure_plot(self):
        plt.title(self.title)
        plt.xlabel(" ".join([self.xchannel, self.xunits]), fontsize=self.fontsize)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.tick_params(which='both', labelsize=15)
        plt.legend()
        plt.grid()

    def plot(self, ychannel, yunits, ydata):
        plt.plot(self.xdata, ydata, label="{} {}".format(ychannel, yunits))
        self._configure_plot()

    def show(self):
        self._configure_plot()
        plt.show()

class Input():
    def __init__(self, filename):
        self.filename = filename
        self.f = open(filename)
        self.units = {}
        self.data = {}

    def _string_to_list(self, string, delimiter=" "):
        dirty = string.split(delimiter)
        clean = list(filter(None, dirty))
        return clean

    def read_data(self, skiplines, delimiter=" "):
        # skip the empty lines at the top
        for _ in range(skiplines):
            self.f.readline()

        # parse the channel names
        line = self.f.readline().replace("\t", delimiter).rstrip("\n")
        channels = self._string_to_list(line, delimiter=delimiter)
        channels = [c.strip(" ") for c in channels]
        for channel in channels:
            self.data[channel] = []

        # parse the units
        line = self.f.readline().replace("\t", " ").rstrip("\n")
        for i, unit in enumerate(self._string_to_list(line, delimiter=delimiter)):
            self.units[channels[i]] = unit

        for line in self.f:
            linelist = self._string_to_list(line.rstrip("\n"), delimiter=delimiter)
            for i, element in enumerate(linelist):
                self.data[channels[i]].append(float(element))

    def plot(self, title, xchannel, ychannels):
        i0, iN = 0, -1
        plot = Plot(title, xchannel, self.units[xchannel], self.data[xchannel][i0:iN])
        for channel in ychannels:
            plot.plot(channel, self.units[channel], self.data[channel][i0:iN])
    
    def show_plots(self):
        plt.show()

if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plots time-series results, typically from OpenFAST.", prog="plotter")
    parser.add_argument(dest="filename", help='Filename for where to get the time-series data.')
    parser.add_argument(dest="title", help='Title for the plot.')
    parser.add_argument(dest="xchannel", help='Name of the x-axis channel.')
    parser.add_argument(dest='ychannels', nargs='+', help='Name of the y-axis channels.')
    parser.add_argument(
        '-s',
        '--skip-lines',
        type=int,
        dest='skiplines',
        help='Lines to skip before channel names.',
        required=False,
        default=6
    )
    args = parser.parse_args()

    input_container = Input(args.filename)
    input_container.read_data(args.skiplines)
    input_container.plot(args.title, args.xchannel, args.ychannels)
    input_container.show_plots()
