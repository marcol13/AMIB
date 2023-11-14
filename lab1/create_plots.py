import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

from collections import defaultdict

class Statistics:
    def __init__(self, filename, popsize=50, gensize=20):
        self.df = pd.DataFrame()
        self.frames = []
        self.filename = filename
        self.popsize = popsize
        self.gensize = gensize

        self.read_data()

    def read_data(self):
        files = os.listdir()
        reg = re.compile(f"^{self.filename}-.*\.csv")
        files = [f for f in files if reg.match(f)]

        self.frames = []
        for f in files:
            temp_df = pd.read_csv(f)
            self.frames.append(temp_df)
        
        self.df = pd.concat(self.frames, axis=0, ignore_index=True)


class Plots:
    def __init__(self, stats=[], gensize=20, popsize=50):
        self.stats = stats
        self.gensize = gensize
        self.popsize = popsize
        self.colors = ["blue", "yellow", "green", "red", "black", "cyan", "magenta"]

    def get_maxes(self):
        maxes = defaultdict(lambda: [])
        for s in self.stats:
            for df in s.frames:
                maxes[df.iloc[0].mutation].append(df["max"].to_list())

        return maxes
    
    def get_hofs(self):
        hofs = defaultdict(lambda: [])
        for s in self.stats:
            for df in s.frames:
                hofs[df.iloc[0].mutation].append(max(df["max"].to_list()))

        return hofs
    
    def get_times(self):
        times = defaultdict(lambda: [])
        for s in self.stats:
            for df in s.frames:
                times[df.iloc[0].mutation].append(df["time"][0])

        return times

    def plot_maxes(self):
        x = [y1 * self.popsize for y1 in range(self.gensize + 1)]
        maxes = self.get_maxes()

        for index, (mut, data) in enumerate(maxes.items()):
            for dy in data:
                plt.plot(x, dy, label=f"mutacja = {mut}", color=self.colors[index])

        handles, labels = plt.gca().get_legend_handles_labels()
        unique_labels = list(set(labels))
        handles = [handles[labels.index(label)] for label in unique_labels]
        
        plt.ylabel("max fitness")
        plt.xlabel("liczba ocenionych osobników")
        plt.legend(handles, unique_labels)
        plt.show()

    def std_dev_plot(self):
        maxes = self.get_maxes()
        x = range(self.gensize + 1)

        for index, (mut, data) in enumerate(maxes.items()):
            mean = np.mean(data, axis=0)
            std_dev = np.std(data, axis=0)
            plt.plot(x, mean, label=f"mutacja = {mut}", color=self.colors[index])
            plt.fill_between(x, mean - std_dev / 3, mean + std_dev / 3, color=self.colors[index], alpha=0.2)

        plt.ylabel("max fitness")
        plt.xlabel("generacja")
        plt.legend()
        plt.show()

    def box_plot(self):
        hofs = self.get_hofs()
        times = self.get_times()
        x = [float(x1) for x1 in hofs.keys()]

        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        ax1.boxplot(hofs.values(), positions=range(len(hofs.keys())))
        ax1.set_xticks(range(len(hofs.keys())), hofs.keys())
        ax1.set_xlabel("mutacja")
        ax1.set_ylabel("hof fitness")

        ax2.boxplot(times.values(), positions=range(len(hofs.keys())))
        ax2.set_xticks(range(len(hofs.keys())), hofs.keys())
        ax2.set_xlabel("mutacja")
        ax2.set_ylabel("czas [s]")
        plt.show()

stat_0 = Statistics("HoF-f9-0", gensize=90)
stat_1 = Statistics("HoF-f9-005", gensize=90)
stat_2 = Statistics("HoF-f9-01", gensize=90)
stat_3 = Statistics("HoF-f9-02", gensize=90)
stat_4 = Statistics("HoF-f9-03", gensize=90)
stat_5 = Statistics("HoF-f9-04", gensize=90)
stat_6 = Statistics("HoF-f9-05", gensize=90)

plots = Plots(stats=[stat_0, stat_1, stat_2, stat_3, stat_4, stat_5, stat_6], gensize=90)
plots.plot_maxes()
plots.std_dev_plot()
plots.box_plot()
