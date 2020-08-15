from tkinter.tix import ScrolledWindow

import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.tix import *
from tkinter import ttk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import copy


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


def get_value_result_param(param, doc_list):
    length = len(doc_list)
    to_return = []
    i = 0
    while i != length:
        direction = doc_list[i]
        direction = direction.replace("\n", "")
        file = open(direction, 'r')
        line_read = file.readlines()
        value = 0
        for lines in line_read:
            if param in lines:
                value = parse_value_line(lines)
                print(value)
                print(param)
        file.close()
        to_return.append(value)
        i += 1
    return to_return


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


def get_all_results(doc_list, params):
    list_to_return = []
    for parameters in params:
        list_to_return.append(get_value_result_param(parameters, doc_list))
    return list_to_return


def array_str_to_int(str_list):
    int_to_return = []
    for string in str_list:
        int_to_return.append(int(string))
    return int_to_return


class DataToGui:
    guiRoot = None
    benchMarksCanvas = []
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
        self.benchCanvas = []

    def create_graph(self, data, names, var_name):
        plot_canvas = Canvas(self.guiRoot, height=500, width=595)
        data1 = {'Benchmark': names,
                 var_name: data}
        df1 = DataFrame(data1, columns=['Benchmark', var_name])
        figure1 = plt.Figure(figsize=(6, len(names)), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, plot_canvas)
        bar1.get_tk_widget().place(height=505, width=600, x=0, y=0)
        df1 = df1[['Benchmark', var_name]].groupby('Benchmark').sum()
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title("Benchmark Vs. " + var_name)
        self.benchMarksGraphs.append([ax1, df1, bar1])
        self.benchCanvas.append([plot_canvas, var_name])
        return ax1

    def set_gui_root(self, root):
        self.guiRoot = root

    def set_benchmarks_names(self, names):
        self.benchMarksNames = names

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
            print(self.benchMarksNames)
            new_graph = self.create_graph(self.benchMarksParametersValues[i], self.benchMarksNames,
                                          self.benchMarksParameters[i])
            self.benchMarksGraphs.append(new_graph)
            i += 1

    def get_canvas_from_name(self, name):
        for array in self.benchCanvas:
            if array[1] == name:
                return array[0]
        return None


def config_graph_holder():
    global graph_holder

    param_lists = parse_document("config.txt")
    graph_holder.set_benchmarks_names(parse_list(param_lists[3]))
    graph_holder.set_benchmarks_param(parse_list(param_lists[1]))
    graph_holder.set_benchmarks_parameters_lines(parse_list(param_lists[2]))
    graph_holder.set_benchmarks_parameters_values(get_all_results(parse_list(param_lists[0]),parse_list( param_lists[1])))
    if graph_holder.guiRoot is not None:
        graph_holder.init_graphics()

def parse_list(list):
    if None in list:
        list.remove(None)
    if "\n" in list:
        list.remove("\n")
    return list

def print_gui_data():
    global graph_holder
    print(graph_holder.benchMarksNames)
    print(graph_holder.benchMarksParameters)
    print(graph_holder.benchMarksParametersLines)
    print(graph_holder.benchMarksGraphsNames)
    print(graph_holder.benchMarksParametersValues)
    print(graph_holder.benchMarksGraphs)


root = None

canvas_prev1 = None
canvas_actual1 = None

variable = None


def callback(*args):
    print(variable.get())
    global canvas_prev1
    global graph_holder
    global canvas_actual1
    if canvas_actual1 is not None:
        canvas_actual1.place(x=-1000, y=0)
        canvas_prev1 = canvas_actual1
        canvas_actual1 = copy.copy(graph_holder.get_canvas_from_name(variable.get()))
        canvas_actual1.place(x=10, y=130)
    else:
        canvas_actual1 = copy.copy(graph_holder.get_canvas_from_name(variable.get()))
        print(canvas_actual1)
        canvas_actual1.place(x=10, y=130)


##############################______________________________________________________________________________________

canvas_actual2 = None
canvas_prev2 = None

variable2 = None


def callback2(*args):
    global canvas_prev2
    global graph_holder
    global canvas_actual2
    if canvas_actual2 is not None:
        canvas_actual2.place(x=-1000, y=0)
        canvas_prev2 = canvas_actual2
        canvas_actual2 = copy.copy(graph_holder.get_canvas_from_name(variable2.get()))
        canvas_actual2.place(x=650, y=130)
    else:
        canvas_actual2 = copy.copy(graph_holder.get_canvas_from_name(variable2.get()))
        canvas_actual2.place(x=650, y=130)


# _______________________________________________________________________________________________________
canvas_actual3 = None
canvas_prev3 = None

variable3 = None


def callback3(*args):
    global canvas_prev3
    global graph_holder
    global canvas_actual3
    if canvas_actual3 is not None:
        canvas_actual3.place(x=-1000, y=0)
        canvas_prev3 = canvas_actual2
        canvas_actual3 = copy.copy(graph_holder.get_canvas_from_name(variable3.get()))
        canvas_actual3.place(x=1300, y=130)
    else:
        canvas_actual3 = copy.copy(graph_holder.get_canvas_from_name(variable3.get()))
        canvas_actual3.place(x=1300, y=130)


def init_interface():
    try:
        global graph_holder
        global root
        global variable3
        global variable
        global variable2
        graph_holder = None
        graph_holder = DataToGui()
        root = tk.Tk()
        root.geometry("1920x1080")
        canvas = Canvas(root, height=1080, width=1920, bg="white")
        canvas.place(x=0, y=-5)
        graph_holder.set_gui_root(canvas)
        config_graph_holder()
        variable = tk.StringVar(canvas)
        variable.set("")
        opt = tk.OptionMenu(canvas, variable, *graph_holder.benchMarksParameters)
        opt.config(width=20, font=('Helvetica', 10))
        opt.place(x=10, y=100)
        variable.trace("w", callback)
        variable2 = tk.StringVar(canvas)
        variable2.set("")
        opt2 = tk.OptionMenu(canvas, variable2, *graph_holder.benchMarksParameters)
        opt2.config(width=20, font=('Helvetica', 10))
        opt2.place(x=650, y=100)
        variable2.trace("w", callback2)
        variable3 = tk.StringVar(canvas)
        variable3.set("")
        opt3 = tk.OptionMenu(canvas, variable3, *graph_holder.benchMarksParameters)
        opt3.config(width=20, font=('Helvetica', 10))
        opt3.place(x=1300, y=100)
        variable3.trace("w", callback3)
        root.mainloop()
    except Exception as e:
        tk.messagebox.showerror("Error, could not find file", "Please check the configuration file")
        print(e)


init_interface()