from tkinter.tix import ScrolledWindow

import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.tix import *
from tkinter import ttk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def parse_document(filename):
    file1 = open(filename, 'r')
    lines = file1.readlines()
    directions = lines[0].split("%")
    params = lines[1].split("%")
    print(directions)
    try:
        directions.remove("\n")
        directions[len(directions) - 1].replace("\n", "")
        params.remove("\n")
        params[len(params) - 1].replace("\n", "")

    except:
        None
    lines_num = array_str_to_int(lines[2].split("%"))
    benchmarks_names = lines[3].split("%")
    return [directions, params, lines_num, benchmarks_names]


def get_value_result(line, doc_list):
    length = len(doc_list)
    to_return = []
    i = 0
    while i != length:
        direction = doc_list[i]
        direction = direction.replace("\n", "")
        file = open(direction, 'r')
        line_read = file.readlines()[line]
        value = parse_value_line(line_read)
        file.close()
        to_return.append(value)
        i += 1
    return to_return


def parse_value_line(line):
    str_to_return = ""
    i = 0
    length = len(line)
    while i != length:
        if line[i] == " ":
            break
        i += 1
    while i != length:
        if line[i] != " ":
            break
        i += 1
    while i != length:
        if line[i] == " ":
            return float(str_to_return)
        str_to_return += line[i]
        i += 1


def get_all_results(doc_list, lines):
    list_to_return = []
    for num_line in lines:
        list_to_return.append(get_value_result(num_line, doc_list))
    return list_to_return


def array_str_to_int(str_list):
    int_to_return = []
    for string in str_list:
        int_to_return.append(int(string))
    return int_to_return


class DataToGui:
    guiRoot = None
    benchMarksNames = []
    benchMarksParameters = []
    benchMarksParametersLines = []
    benchMarksGraphsNames = []
    benchMarksParametersValues = []
    benchMarksGraphs = []

    def __init__(self):
        self.guiRoot = None
        self.benchMarksNames = []
        self.benchMarksParameters = []
        self.benchMarksParametersLines = []
        self.benchMarksGraphsNames = []
        self.benchMarksParametersValues = []
        self.benchMarksGraphs = []

    def create_graph(self, data, names, var_name):
        data1 = {'Benchmark': names,
                 var_name: data}
        df1 = DataFrame(data1, columns=['Benchmark', var_name])
        figure1 = plt.Figure(figsize=(6, len(names)), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.guiRoot)
        bar1.get_tk_widget().place(height=400, width=400,x=0,y=0)
        #bar1.get_tk_widget().pack(side=LEFT, fill=tk.BOTH)
       #bar1.get_tk_widget().pack()
        df1 = df1[['Benchmark', var_name]].groupby('Benchmark').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title("Benchmark Vs. " + var_name)
        self.benchMarksGraphs.append([ax1, df1, bar1])
        return ax1

    def set_gui_root(self, root):
        self.guiRoot = root

    def set_benchmarks_names(self, names):
        self.benchMarksParameters = names

    def set_benchmarks_param(self, params):
        self.benchMarksParameters = params

    def set_benchmarks_graphs_names(self, names):
        self.benchMarksGraphsNames = names

    def add_benchmarks_graphs(self, graph):
        self.benchMarksGraphs.append(graph)

    def reset_graphs(self):
        self.guiRoot = tk(self.guiRoot)
        for child in self.guiRoot.winfo_children():
            child.destroy()

    def add_benchmarks_parameters_values(self, values):
        self.benchMarksParametersValues.append(values)

    def set_benchmarks_parameters_values(self, values):
        self.benchMarksParametersValues = values

    def set_benchmarks_parameters_lines(self, lines):
        self.benchMarksParametersLines = lines

    def init_graphics(self):
        length = len(self.benchMarksParameters)
        i = 0
        while i != length:
            new_graph = self.create_graph(self.benchMarksParametersValues[i], ["lol", "lol2", "lol3"],
                                          self.benchMarksParameters[i])
            self.benchMarksGraphs.append(new_graph)
            i += 1


graph_holder = DataToGui()


def config_graph_holder():
    global graph_holder

    param_lists = parse_document("config.txt")
    graph_holder.set_benchmarks_names(param_lists[3])
    graph_holder.set_benchmarks_param(param_lists[1])
    graph_holder.set_benchmarks_parameters_lines(param_lists[2])
    graph_holder.set_benchmarks_parameters_values(get_all_results(param_lists[0], param_lists[2]))
    if graph_holder.guiRoot is not None:
        graph_holder.init_graphics()


def print_gui_data():
    global graph_holder
    print(graph_holder.benchMarksNames)
    print(graph_holder.benchMarksParameters)
    print(graph_holder.benchMarksParametersLines)
    print(graph_holder.benchMarksGraphsNames)
    print(graph_holder.benchMarksParametersValues)
    print(graph_holder.benchMarksGraphs)


root = tk.Tk()
root.geometry("400x400")
canvas  = Canvas ( root, height = 400, width=400 )
canvas.pack()
graph_holder.set_gui_root(canvas)
config_graph_holder()

print_gui_data()

root.mainloop()
