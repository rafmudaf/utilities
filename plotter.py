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

    def read_data(self):
        # skip the empty lines at the top
        for _ in range(6):
            self.f.readline()

        # parse the channel names
        line = self.f.readline().replace("\t", " ").rstrip("\n")
        channels = self._string_to_list(line)
        for channel in channels:
            self.data[channel] = []

        # parse the units
        line = self.f.readline().replace("\t", " ").rstrip("\n")
        for i, unit in enumerate(self._string_to_list(line)):
            self.units[channels[i]] = unit

        for line in self.f:
            linelist = self._string_to_list(line.rstrip("\n"), "\t")
            for i, element in enumerate(linelist):
                self.data[channels[i]].append(float(element))

    def plot(self, title, xchannel, ychannels):
        plot = Plot(title, xchannel, self.units[xchannel], self.data[xchannel])
        for channel in ychannels:
            plot.plot(channel, self.units[channel], self.data[channel])
        # plt.show()
    
    def show_plots(self):
        plt.show()

if __name__=="__main__":
    import sys
    if len(sys.argv) < 4:
        print("Input error. Usage: ./plotter filename title xchannel ychannel1 ychannel2 ... ychannelN")
    else:
        filename = sys.argv[1]
        title = sys.argv[2]
        xchannel = sys.argv[3]
        ychannels = sys.argv[4:]
        input_container = Input(filename)
        input_container.read_data()
        input_container.plot(title, xchannel, ychannels)
        input_container.show_plots()
