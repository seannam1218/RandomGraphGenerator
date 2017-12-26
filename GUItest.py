from tkinter import *
from tkinter import messagebox

from Graph import *

#constants for the window:
WIDTH = 1000
HEIGHT = 600
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

#setting up tkinter canvas
root = Tk()
CANVAS_BG = "aquamarine"
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg = CANVAS_BG)

def onButtonPress():
    if v_entry.get() == "" or e_entry.get() == "":
        messagebox.showinfo("Information", "Please fill in the entry boxes for the number of vertices and edges.")
        return
    v.set(v_entry.get())
    e.set(e_entry.get())
    #check for entries that cause errors
    if v.get() > 24 or v.get() < 1:
        messagebox.showinfo("Information", "Minimum number of vertices is 1; Maximum number of vertices is 22.")
        return
    canvas.delete("all")
    # canvas.delete("all") doesn't take care of labels.
    # manually removes all the labels made.
    for l in labelArray:
        l[0].place_forget()
    labelArray.clear()

    generate_graph(v.get(), e.get())

generate_button = Button(canvas, text="Generate", command=onButtonPress)
generate_button.place(x=WIDTH/8, y=HEIGHT/2)

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

weight_option = StringVar()
weight_option.set("Weighted: off") # initial value
options = ["Weighted: off", "Weighted: Gaussian-distributed weights", "Weighted: randomly distributed weights"]
def onOptionClick(option):
    if weight_option.get() == "Weighted: off":
        wt_entry1_name.set("")
        wt_entry1_label.config(text = wt_entry1_name.get())
        wt_entry2_name.set("")
        wt_entry2_label.config(text=wt_entry2_name.get())
    elif weight_option.get() == "Weighted: Gaussian-distributed weights":
        wt_entry1_name.set("Mean")
        wt_entry1_label.config(text=wt_entry1_name.get())
        wt_entry2_name.set("Standard deviation")
        wt_entry2_label.config(text=wt_entry2_name.get())
    elif weight_option.get() == "Weighted: randomly distributed weights":
        wt_entry1_name.set("Min")
        wt_entry1_label.config(text=wt_entry1_name.get())
        wt_entry2_name.set("Max")
        wt_entry2_label.config(text=wt_entry2_name.get())

option = OptionMenu(canvas, weight_option, *(options), command=onOptionClick)
option.place(x=WIDTH/5 - 130, y=HEIGHT/10 + LINE*6)

wt_entry1 = Entry(canvas, width=5)
wt_entry1.place(x=WIDTH/5, y=HEIGHT/10+LINE*8)
wt_entry2 = Entry(canvas, width=5)
wt_entry2.place(x=WIDTH/5, y=HEIGHT/10+LINE*9)

wt_entry1_name = StringVar()
wt_entry1_name.set("Mean: ")
wt_entry2_name = StringVar()
wt_entry2_name.set("Standard deviation: ")

wt_entry1_label = Label(canvas, text = wt_entry1_name.get(), bg = CANVAS_BG)
wt_entry1_label.place(x=WIDTH/5 - 130, y=HEIGHT/10+LINE*8)
wt_entry2_label = Label(canvas, text = wt_entry2_name.get(), bg = CANVAS_BG)
wt_entry2_label.place(x=WIDTH/5 - 130, y=HEIGHT/10+LINE*9)

v = IntVar()
e = IntVar()
v.set(2)
e.set(2)

def generate_graph(v, e):
    # generate graph
    graph = Graph(v, e, loops.get())

    graph.directed = directed.get()
   # graph.weighted = weighted.get()

    graph.makeGraph()
    vertexPosArray = []

    #draw vertices
    for i in range(0, graph.v):
        v_x = X_CENTER + R * sin(2 * pi * i / graph.v)
        v_y = Y_CENTER - R * cos(2 * pi * i / graph.v)
        v_pos = [v_x, v_y]
        vertexPosArray.append(v_pos)
        draw_vertex(graph.vertexArray[i], X_CENTER + R * sin(2 * pi * i / graph.v),
                    Y_CENTER - R * cos(2 * pi * i / graph.v), VERTEX_RADIUS)

    if (graph.weighted == True):
        graph.generateWeights()

    #draw edges
    for i in range(0, graph.e):
        vertex1_index = ord(graph.edgeArray[i][0]) - 97
        vertex2_index = ord(graph.edgeArray[i][1]) - 97

        x1 = vertexPosArray[vertex1_index][0]
        y1 = vertexPosArray[vertex1_index][1]
        x2 = vertexPosArray[vertex2_index][0]
        y2 = vertexPosArray[vertex2_index][1]
        draw_edge(x1, y1, x2, y2, graph.directed)

        if (graph.weighted == True):
            if (graph.edgeArray[i][0] != graph.edgeArray[i][1]):
                dx = x2 - x1
                dy = y2 - y1
                factor = avoid_collision(x1, y1, x2, y2, 0.6)
                draw_label(graph.weightArray[i], 7, x1+factor*dx + 1, y1+factor*dy, CANVAS_BG)
            else:
                dx = X_CENTER - x1
                dy = Y_CENTER - y1
                draw_label(graph.weightArray[i], 7, x1-0.18*dx, y1-0.18*dy, CANVAS_BG)

    # print vertex set and edge set onto console.
    graph.printGraph()
    # if weighted == True, print weights
    graph.printWeights()
    print("")

def avoid_collision(x1, y1, x2, y2, def_factor):
    ret = def_factor
    for l in labelArray:
        # if location of label collides with another existing label, change def_factor
        if (l[1] > x1+def_factor*(x2-x1)-5) and (l[1] < x1+def_factor*(x2-x1)+5) and (l[2] > y1+def_factor*(y2-y1)-5) and (l[2] < y1+def_factor*(y2-y1)+5):
            ret = avoid_collision(x1, y1, x2, y2, def_factor-0.03) #or ret-0.03 if you want to move just one.
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
    # make a frame to allow customization of label size
    #frame = Frame(canvas, width=w, height=h, bg=bg)
    #frame.place(x=x-w/2, y=y-h/2)
    # make label and pack it on frame.
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
    #draw_label(name, x, y, VERTEX_COLOR, VERTEX_LABEL_WIDTH, VERTEX_LABEL_HEIGHT)
    draw_label(name, 11, x, y, VERTEX_COLOR)


canvas.pack()
root.mainloop()