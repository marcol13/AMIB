import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

from collections import defaultdict

class Statistics:
    def __init__(self, filename, popsize=50, gensize=20, dir="."):
        self.df = pd.DataFrame()
        self.frames = []
        self.filename = filename
        self.popsize = popsize
        self.gensize = gensize

        self.read_data(dir)

    def read_data(self, dir):
        files = os.listdir(dir)
        reg = re.compile(f"^{self.filename}-.*\.csv")
        files = [f"{dir}/{f}" for f in files if reg.match(f)]

        self.frames = []
        for f in files:
            temp_df = pd.read_csv(f)
            self.frames.append(temp_df)
        
        self.df = pd.concat(self.frames, axis=0, ignore_index=True)
        print(self.df)


class Plots:
    def __init__(self, stats=[], gensize=20, popsize=50):
        self.stats = stats
        self.gensize = gensize
        self.popsize = popsize
        self.colors = ["blue", "yellow", "green", "red", "black", "cyan", "magenta", "gray"]

    def get_maxes(self):
        maxes = defaultdict(lambda: [])
        for s in self.stats:
            for df in s.frames:
                maxes[f"{df.iloc[0].method}_{df.iloc[0].format}"].append(df["max"].to_list())

        return maxes
    
    def get_hofs(self):
        hofs = defaultdict(lambda: [])
        for s in self.stats:
            for df in s.frames:
                hofs[f"{df.iloc[0].method}_{df.iloc[0].format}"].append(max(df["max"].to_list()))

        return hofs
    
    def get_times(self):
        times = defaultdict(lambda: [])
        for s in self.stats:
            for df in s.frames:
                times[f"{df.iloc[0].method}_{df.iloc[0].format}"].append(df["time"][0])

        return times

    def plot_maxes(self):
        x = [y1 * self.popsize for y1 in range(self.gensize + 1)]
        maxes = self.get_maxes()

        for index, (rep, data) in enumerate(maxes.items()):
            method, format = rep.split("_")
            method = int(float(method))
            format = int(float(format))

            for dy in data:
                plt.plot(x, dy, label=f"f{format} {'(extended)' if method == 1 else '(basic)'}", color=self.colors[index])

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

        for index, (rep, data) in enumerate(maxes.items()):
            method, format = rep.split("_")
            method = int(float(method))
            format = int(float(format))

            mean = np.mean(data, axis=0)
            std_dev = np.std(data, axis=0)
            plt.plot(x, mean, label=f"f{format} {'(extended)' if method == 1 else '(basic)'}", color=self.colors[index])
            plt.fill_between(x, mean - std_dev / 3, mean + std_dev / 3, color=self.colors[index], alpha=0.2)

        plt.ylabel("max fitness")
        plt.xlabel("generacja")
        plt.legend()
        plt.show()

    def box_plot(self):
        hofs = self.get_hofs()
        times = self.get_times()
        x1 = [x1.split("_")[1] for x1 in hofs.keys()]
        x1 = [int(float(xt)) for xt in x1]

        _, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        bp = ax1.boxplot(hofs.values(), positions=range(len(hofs.keys())), patch_artist=True)
        colors = ["green", "red"]

        legend_labels = ["basic", "extended"]
        legend_patches = [plt.Rectangle((0,0),1,1,fc=color, edgecolor='none') for color in colors]

        for i_box, box in enumerate(bp['boxes']):
            color = colors[0] if i_box % 2 == 0 else colors[1]
            box.set_color(color)


        ax1.set_xticks(range(len(hofs.keys())), x1)
        ax1.set_xlabel("reprezentacja f")
        ax1.set_ylabel("hof fitness")
        ax1.legend(legend_patches, legend_labels, loc="upper right")

        bp = ax2.boxplot(times.values(), positions=range(len(hofs.keys())), patch_artist=True)

        for i_box, box in enumerate(bp['boxes']):
            color = "green" if i_box % 2 == 0 else "red"
            box.set_color(color)

        ax2.set_xticks(range(len(hofs.keys())), x1)
        ax2.set_xlabel("reprezentacja f")
        ax2.set_ylabel("czas [s]")
        ax2.legend(legend_patches, legend_labels, loc="upper right")

        plt.show()

stat_0 = Statistics("HoF-0", gensize=90, dir="lab2")
stat_1 = Statistics("HoF-1", gensize=90, dir="lab2")
stat_2 = Statistics("HoF-4", gensize=90, dir="lab2")
stat_3 = Statistics("HoF-9", gensize=90, dir="lab2")
# stat_0 = Statistics("HoF-", gensize=20, dir="lab2")
# stat_1 = Statistics("HoF-f9-005", gensize=90)
# stat_2 = Statistics("HoF-f9-01", gensize=90)
# stat_3 = Statistics("HoF-f9-02", gensize=90)
# stat_4 = Statistics("HoF-f9-03", gensize=90)
# stat_5 = Statistics("HoF-f9-04", gensize=90)
# stat_6 = Statistics("HoF-f9-05", gensize=90)

# plots = Plots(stats=[stat_0, stat_1, stat_2, stat_3, stat_4, stat_5, stat_6], gensize=20)
plots = Plots(stats=[stat_0, stat_1, stat_2, stat_3], gensize=90)
plots.plot_maxes()
plots.std_dev_plot()
plots.box_plot()
