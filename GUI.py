from tkinter import *
from tkinter import messagebox
from time import strftime
import os.path

from Graph import *

#constants for the window:
WIDTH = 1200
HEIGHT = 700
LINE = 20

#constants for graph part of the visualization
X_CENTER = WIDTH*2/3
Y_CENTER = HEIGHT/2
R = min(WIDTH, HEIGHT)*0.4

# constants for vertices and edges representations
VERTEX_RADIUS = 15
VERTEX_COLOR = "yellow"

# constants for labels
VERTEX_LABEL_HEIGHT = 15
VERTEX_LABEL_WIDTH = 12
labelArray = []
#stores the trajectories of edges, each divided into 40 pieces -> for the purposes of avoiding label collision
coordinatesArray = []

#setting up tkinter canvas
root = Tk()
CANVAS_BG = "aquamarine"
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg = CANVAS_BG)

def onGenerateButtonPress():
    if v_entry.get() == "" or e_entry.get() == "":
        messagebox.showinfo("Information", "Please fill in the entry boxes for the number of vertices and edges.")
        return
    v.set(v_entry.get())
    e.set(e_entry.get())

    #check for entries that cause errors
    if v.get() > 20 or v.get() < 1:
        messagebox.showinfo("Information", "Minimum number of vertices is 1; Maximum number of vertices is 20.")
        return

    #for unigraphs
    if multigraph.get() == False:
        if e.get() > v.get()*(v.get()-1)/2 and loops.get() == False:
            messagebox.showinfo("Information", "Maximum number of edges for a loopless unigraph of " + str(v.get()) + " vertices is " + str(v.get()*(v.get()-1)/2) + ".")
            return
        if e.get() > (v.get()*(v.get()-1)/2 + v.get()) and loops.get() == True:
            messagebox.showinfo("Information", "Maximum number of edges for a unigraph with loops of " + str(v.get()) + " vertices is " + str((v.get()*(v.get()-1)/2) + v.get()) + ".")
            return

    if weight_option.get() == "Weighted: Gaussian-distributed weights":
        if wt_entry1.get() == "" or wt_entry2.get() == "":
            messagebox.showinfo("Information", "Please fill in the entry boxes for mean and standard deviation of weight values.")
            return
        if allow_negative.get() == False and int(wt_entry1.get()) < 0:
            messagebox.showinfo("Information", "Mean value for Gaussian distribution cannot be smaller than 0 when negative values are not allowed.")
            return
    elif weight_option.get() == "Weighted: randomly distributed weights":
        if wt_entry1.get() == "" or wt_entry2.get() == "":
            messagebox.showinfo("Information", "Please fill in the entry boxes for min and max weight values.")
            return
        if int(wt_entry1.get()) > int(wt_entry2.get()):
            messagebox.showinfo("Information", "Min value must be smaller or equal to max value")
            return
        if allow_negative.get() == False and int(wt_entry1.get()) < 0:
            messagebox.showinfo("Information", "When negative values are not allowed, min value must be greater than 0")
            return

    canvas.delete("all")
    # canvas.delete("all") doesn't take care of labels.
    # manually removes all the labels made.
    for l in labelArray:
        l[0].place_forget()
    labelArray.clear()

    generate_graph(v.get(), e.get())

generate_button = Button(canvas, text="Generate", command=onGenerateButtonPress)
generate_button.place(x=WIDTH/5- 130, y=HEIGHT/10+ 13*LINE)

def onSaveButtonPress():
    if graph == None:
        messagebox.showinfo("Information", "Please generate a graph before saving.")
        return
    #make directory named "saved" is it doesn't already exist
    if not os.path.exists("saved graphs"):
        os.makedirs("saved graphs")

    time = strftime("%Y_%m_%d")
    n = 0
    while (os.path.isfile("saved graphs/" + time + '.txt') == True):
        n += 1
        time = strftime("%Y_%m_%d") + "(" + str(n) + ")"

    f = open("saved graphs/" + time + '.txt', 'w')
    f.write("Vertices = " + str(graph.vertexArray) + "\n" + "Edges = " + str(graph.edgeArray) + "\n")
    f.write("Weights = " + str(graph.weightArray) + "\n")

    #for meta-information
    f.write("\n //the following is a list of meta-information for the purposes of loading a saved project.\n")
    f.write("//" + str(graph.v) + ";" + str(graph.e) + ";" + str(graph.allow_loops) + ";" + str(graph.directed) + ";" + str(graph.multi) + ";" + str(weight_option.get()) + ";" + str(wt_entry1.get()) + ";" + str(wt_entry2.get()) + ";" + str(graph.allow_negative) + ";")

    f.close()
    messagebox.showinfo("Information", "Current graph was saved in the following directory:\n ../saved graphs/" + time + ".txt")

save_button = Button(canvas, text="Save", command=onSaveButtonPress)
save_button.place(x=WIDTH / 5 - 60, y=HEIGHT / 10 + 13 * LINE)

def onLoadButtonPress():
    try:
        f = open("saved graphs/" + filename_entry.get() + '.txt', 'r')
    except:
        messagebox.showinfo("Information", filename_entry.get() + ".txt does not exist in the directory.")
        return
    # stores vertex array read from file into tempVArray
    f.readline(11)
    vertices_txt = f.readline()
    tempVArray = []
    for char in vertices_txt:
        if char.isalpha():
            tempVArray.append(char)

    # stores edge array read from file into tempEArray
    f.readline(8)
    edges_txt = f.readline()
    tempEArray = []
    tempE = []
    for char in edges_txt:
        if char.isalpha():
            if len(tempE) <= 1:
                tempE.append(char)
            else:
                tempEArray.append(tempE)
                tempE = [char]
    tempEArray.append(tempE)
    # stores weight array read from file into tempWArray
    f.readline(9)
    weights_txt = f.readline()
    tempWArray = []
    weight = ""
    for char in weights_txt:
        if char != "," and char != " " and char != "[" and char != "]":
            weight = weight + char
        else:
            if weight != "":
                tempWArray.append(float(weight))
            weight = ""

    # read off metadata to construct graph from
    for i in range(2):
        f.readline()
    f.readline(2)
    txt = f.readline()
    data = ""
    dataArray = []
    for char in txt:
        if char != ";":
            data = data + char
        else:
            try:
                data = int(data)
            except:
                if data == "True":
                    data = True
                elif data == "False":
                    data = False
            dataArray.append(data)
            data = ""

    graph = Graph(dataArray[0], dataArray[1], dataArray[2])
    v_entry.delete(0,END)
    v_entry.insert(0, str(dataArray[0]))
    e_entry.delete(0, END)
    e_entry.insert(0, str(dataArray[1]))
    graph.vertexArray = tempVArray
    graph.edgeArray = tempEArray
    graph.weightArray = tempWArray
    graph.allow_loops = dataArray[2]
    loops.set(dataArray[2])
    loops_check.deselect()
    if (dataArray[2] == True):
        loops_check.select()
    graph.directed = dataArray[3]
    directed.set(dataArray[3])
    directed_check.deselect()
    if (dataArray[3] == True):
        directed_check.select()
    graph.multi = dataArray[4]
    multigraph.set(dataArray[4])
    multigraph_check.deselect()
    if (dataArray[4] == True):
        multigraph_check.select()
    graph.weighted = dataArray[5]
    weight_option.set(dataArray[5])
    wt_entry1.delete(0, END)
    wt_entry1.insert(0, str(dataArray[6]))
    wt_entry2.delete(0, END)
    wt_entry2.insert(0, str(dataArray[7]))
    graph.allow_negative = dataArray[8]
    allow_negative.set(dataArray[8])
    allow_negative_check.deselect()
    if (dataArray[8] == True):
        allow_negative_check.select()

    canvas.delete("all")
    # canvas.delete("all") doesn't take care of labels.
    # manually removes all the labels made.
    for l in labelArray:
        l[0].place_forget()

    draw_graph(graph)
    graph.printGraph()


load_entry_label = Label(canvas, text = "../saved graphs/", bg = CANVAS_BG)
load_entry_label.place(x=WIDTH / 5 - 130, y=HEIGHT / 10 + 17 * LINE)
load_entry_label2 = Label(canvas, text = ".txt", bg = CANVAS_BG)
load_entry_label2.place(x=WIDTH / 5 + 50, y=HEIGHT / 10 + 17 * LINE)

filename_entry = Entry(canvas, width=14)
filename_entry.place(x=WIDTH/5 - 40, y=HEIGHT/10+LINE*17)

load_button = Button(canvas, text="Load", command=onLoadButtonPress)
load_button.place(x=WIDTH / 5 - 130, y=HEIGHT / 10 + 18 * LINE)

v_entry = Entry(canvas, width=5)
v_entry.place(x=WIDTH/5, y=HEIGHT/10)
e_entry = Entry(canvas, width=5)
e_entry.place(x=WIDTH/5, y=HEIGHT/10+LINE)

entry_label_vertex = Label(canvas, text = "Number of vertices:", bg = CANVAS_BG)
entry_label_vertex.place(x=WIDTH/5 - 130, y=HEIGHT/10)

entry_label_edge = Label(canvas, text = "Number of vertices:", bg = CANVAS_BG)
entry_label_edge.place(x=WIDTH/5 - 130, y=HEIGHT/10+LINE)

loops = BooleanVar()
loops.set(False)
loops_check = Checkbutton(canvas, text = "allow loops", variable = loops, onvalue="True", offvalue="False", bg = CANVAS_BG)
loops_check.place(x=WIDTH/5 - 130, y=HEIGHT/10 + LINE*3)

directed = BooleanVar()
directed.set(False)
directed_check = Checkbutton(canvas, text = "directed", variable = directed, onvalue="True", offvalue="False", bg = CANVAS_BG)
directed_check.place(x=WIDTH/5 - 130, y=HEIGHT/10 + LINE*4)

multigraph = BooleanVar()
multigraph.set(False)
multigraph_check = Checkbutton(canvas, text = "multigraph (visualization not supported)", variable = multigraph, onvalue="True", offvalue="False", bg = CANVAS_BG)
multigraph_check.place(x=WIDTH/5 - 130, y=HEIGHT/10 + LINE*5)

weight_option = StringVar()
weight_option.set("Weighted: off") # initial value
options = ["Weighted: off", "Weighted: Gaussian-distributed weights", "Weighted: randomly distributed weights"]

def onOptionClick(option):
    if weight_option.get() == "Weighted: off":
        wt_entry1_name.set("N/A")
        wt_entry1_label.config(text = wt_entry1_name.get())
        wt_entry2_name.set("N/A")
        wt_entry2_label.config(text=wt_entry2_name.get())
    elif weight_option.get() == "Weighted: Gaussian-distributed weights":
        wt_entry1_name.set("Mean")
        wt_entry1_label.config(text=wt_entry1_name.get())
        wt_entry2_name.set("St_dev")
        wt_entry2_label.config(text=wt_entry2_name.get())
    elif weight_option.get() == "Weighted: randomly distributed weights":
        wt_entry1_name.set("Min")
        wt_entry1_label.config(text=wt_entry1_name.get())
        wt_entry2_name.set("Max")
        wt_entry2_label.config(text=wt_entry2_name.get())

option = OptionMenu(canvas, weight_option, *(options), command=onOptionClick)
option.place(x=WIDTH/5 - 130, y=HEIGHT/10 + LINE*7)

allow_negative = BooleanVar()
allow_negative.set(False)
allow_negative_check = Checkbutton(canvas, text = "allow negative weights", variable = allow_negative, onvalue="True", offvalue="False", bg = CANVAS_BG)
allow_negative_check.place(x=WIDTH/5 - 30, y=HEIGHT/10 + LINE*9)

wt_entry1 = Entry(canvas, width=5)
wt_entry1.place(x=WIDTH/5-80, y=HEIGHT/10+LINE*9)
wt_entry2 = Entry(canvas, width=5)
wt_entry2.place(x=WIDTH/5-80, y=HEIGHT/10+LINE*10)

wt_entry1_name = StringVar()
wt_entry1_name.set("N/A")
wt_entry2_name = StringVar()
wt_entry2_name.set("N/A")

wt_entry1_label = Label(canvas, text = wt_entry1_name.get(), bg = CANVAS_BG)
wt_entry1_label.place(x=WIDTH/5 - 130, y=HEIGHT/10+LINE*9)
wt_entry2_label = Label(canvas, text = wt_entry2_name.get(), bg = CANVAS_BG)
wt_entry2_label.place(x=WIDTH/5 - 130, y=HEIGHT/10+LINE*10)

v = IntVar()
e = IntVar()
v.set(2)
e.set(2)

graph = None

def generate_graph(v, e):
    # generate graph
    global graph
    graph = Graph(v, e, loops.get())

    graph.directed = directed.get()
    graph.multi = multigraph.get()
    if graph.multi==True:
        messagebox.showinfo("Information", "Visualization for multigraphs is not supported. Vertices, edges and weights were generated and are available for saving.")

    graph.makeGraph()
    draw_graph(graph)
    # print vertex set and edge set (and weight set) onto console.
    graph.printGraph()


def draw_graph(graph):
    vertexPosArray = []
    # draw vertices
    for i in range(0, graph.v):
        v_x = X_CENTER + R * sin(2 * pi * i / graph.v)
        v_y = Y_CENTER - R * cos(2 * pi * i / graph.v)
        v_pos = [v_x, v_y]
        vertexPosArray.append(v_pos)
        draw_vertex(graph.vertexArray[i], X_CENTER + R * sin(2 * pi * i / graph.v),
                    Y_CENTER - R * cos(2 * pi * i / graph.v), VERTEX_RADIUS)

    # weights generation
    if weight_option.get() == "Weighted: off":
        graph.weighted = False
        graph.weightArray = []
    elif weight_option.get() == "Weighted: Gaussian-distributed weights":
        graph.weighted = True
        wt_entry1_name.set("Mean")
        wt_entry1_label.config(text=wt_entry1_name.get())
        wt_entry2_name.set("St_dev")
        wt_entry2_label.config(text=wt_entry2_name.get())

        if allow_negative.get() == True:
            graph.allow_negative = True
            graph.generateWeights("gaussian", int(wt_entry1.get()), int(wt_entry2.get()))
        elif allow_negative.get() == False:
            graph.allow_negative = False
            graph.generateWeights("gaussian", int(wt_entry1.get()), int(wt_entry2.get()))

    elif weight_option.get() == "Weighted: randomly distributed weights":
        graph.weighted = True
        wt_entry1_name.set("Min")
        wt_entry1_label.config(text=wt_entry1_name.get())
        wt_entry2_name.set("Max")
        wt_entry2_label.config(text=wt_entry2_name.get())
        if allow_negative.get() == True:
            graph.generateWeights("random", int(wt_entry1.get()), int(wt_entry2.get()))
        elif allow_negative.get() == False:
            graph.generateWeights("random", int(wt_entry1.get()), int(wt_entry2.get()))

    # draw edges
    if graph.multi == False:

        for i in range(0, graph.e):
            vertex1_index = ord(graph.edgeArray[i][0]) - 97
            vertex2_index = ord(graph.edgeArray[i][1]) - 97

            x1 = vertexPosArray[vertex1_index][0]
            y1 = vertexPosArray[vertex1_index][1]
            x2 = vertexPosArray[vertex2_index][0]
            y2 = vertexPosArray[vertex2_index][1]
            draw_edge(x1, y1, x2, y2, graph.directed)

            dx = x2 - x1
            dy = y2 - y1

            if (graph.weighted == True):
                # for edges that are not loops
                if (graph.edgeArray[i][0] != graph.edgeArray[i][1]):
                    if (len(graph.edgeArray) < 25):
                        try:
                            factor = avoid_collision(x1, y1, x2, y2, 0.3)
                        except:
                            # coordinatesArray.clear()
                            factor = avoid_collision2(x1, y1, x2, y2, 0.3)
                        draw_label(graph.weightArray[i], 7, x1 + factor * dx, y1 + factor * dy, CANVAS_BG)
                    else:
                        try:
                            factor = avoid_collision2(x1, y1, x2, y2, 0.3)
                        except:
                            factor = random() * 0.4 + 0.3
                        draw_label(graph.weightArray[i], 7, x1 + factor * dx, y1 + factor * dy, CANVAS_BG)
                # for loops
                else:
                    dx = X_CENTER - x1
                    dy = Y_CENTER - y1
                    draw_label(graph.weightArray[i], 7, x1 - 0.18 * dx, y1 - 0.18 * dy, CANVAS_BG)

            for j in range(50):
                coordinates = []
                coordinates.append(round(x1 + (j / 50) * dx))
                coordinates.append(round(y1 + (j / 50) * dy))
                coordinatesArray.append(coordinates)

        # after calculation, empty coordinatesArray
        coordinatesArray.clear()

def avoid_collision(x1, y1, x2, y2, factor):
    ret = factor
    x = x1 + ret * (x2 - x1)
    y = y1 + ret * (y2 - y1)
    n = 12
    for i in range(len(coordinatesArray)):
        if (x > coordinatesArray[i][0] - n) and (x < coordinatesArray[i][0] + n+5) and (y > coordinatesArray[i][1] - n) and (y < coordinatesArray[i][1] + n+5):
            ret = avoid_collision(x1, y1, x2, y2, random()*0.4 + 0.3)
    return ret

def avoid_collision2(x1, y1, x2, y2, factor):
    ret = factor
    x = x1 + ret * (x2 - x1)
    y = y1 + ret * (y2 - y1)
    for l in labelArray:
        # if location of label collides with another existing label, change def_factor
        if (x < l[1]+17) and (x > l[1]-12) and (y < l[2]+12) and (y > l[2]-12):
            ret = avoid_collision2(x1, y1, x2, y2, ret+0.03)
        if ret > 0.9 or ret < 0.2:
            ret = random()*0.4+0.3
    return ret

#draws loops by drawing an arc on the outer periphery of the graph:
def draw_loop(x, y, r, s, e):
    canvas.create_arc(x - r, y - r, x + r, y + r, start = s, extent = e, style = "arc")

# x1,y1,x2,y2, are positions of vertex 1 and 2.
def draw_edge(x1, y1, x2, y2, dir):
    # building loops
    if (round(x1, 3) == round(x2, 3)) and (round(y1, 3) == round(y2, 3)):
        if (x1 >= X_CENTER):
            if (y1 <= Y_CENTER):
                angle = 360 - degrees(atan((Y_CENTER - y1)/(x1 - X_CENTER + 0.0001)))
            elif (y1 > Y_CENTER):
                angle = degrees(atan((y1 - Y_CENTER)/(x1 - X_CENTER + 0.0001)))
        elif (x1 < X_CENTER):
            if (y1 <= Y_CENTER):
                angle = 180 + degrees(atan((Y_CENTER - y1)/(X_CENTER - x1 + 0.0001)))
            elif (y1 > Y_CENTER):
                angle = 180 - degrees(atan((y1 - Y_CENTER)/(X_CENTER - x1 + 0.0001)))

        dx = (x1-X_CENTER)*0.1
        dy = (y1-Y_CENTER)*0.1
        draw_loop(x1+dx, y1+dy, VERTEX_RADIUS*1.3, 180-angle-45, -360+90)

    # building normal edges
    else:
        if round(x2, 3) == round(x1, 3):
            dx = 0
            dy = VERTEX_RADIUS
        elif round(y2, 3) == round(y1, 3):
            dx = VERTEX_RADIUS
            dy = 0
        else:
            angle = abs(atan((y2 - y1) / (x2 - x1)))
            dx = abs(VERTEX_RADIUS * cos(angle))
            dy = abs(VERTEX_RADIUS * sin(angle))

        if dir == True:
            if x1 < x2:
                if y1 < y2:
                    canvas.create_line(x1 + dx, y1 + dy, x2 - dx, y2 - dy, arrow = LAST)
                if y1 >= y2:
                    canvas.create_line(x1 + dx, y1 - dy, x2 - dx, y2 + dy, arrow = LAST)
            if x1 >= x2:
                if y1 < y2:
                    canvas.create_line(x1 - dx, y1 + dy, x2 + dx, y2 - dy, arrow = LAST)
                if y1 >= y2:
                    canvas.create_line(x1 - dx, y1 - dy, x2 + dx, y2 + dy, arrow = LAST)
        else:
            if x1 < x2:
                if y1 < y2:
                    canvas.create_line(x1 + dx, y1 + dy, x2 - dx, y2 - dy)
                if y1 >= y2:
                    canvas.create_line(x1 + dx, y1 - dy, x2 - dx, y2 + dy)
            if x1 >= x2:
                if y1 < y2:
                    canvas.create_line(x1 - dx, y1 + dy, x2 + dx, y2 - dy)
                if y1 >= y2:
                    canvas.create_line(x1 - dx, y1 - dy, x2 + dx, y2 + dy)


# draws label of given name centered on x and y coordinates
def draw_label(name, fontsize, x, y, bg):
    var = StringVar()
    label = Label(canvas, textvariable = var, bg = bg, font=("Arial", fontsize))
    label.place(x=x-6, y=y-9)
    labelArray.append([label, x, y])
    var.set(name)

# draws vertex centered around x, y coordinates
def draw_vertex(name, x, y, r):
    # draw vertices
    canvas.create_oval(x-r, y-r, x+r, y+r, fill = VERTEX_COLOR)
    # draw labels for the vertices
    draw_label(name, 11, x, y, VERTEX_COLOR)

canvas.pack()
root.mainloop()