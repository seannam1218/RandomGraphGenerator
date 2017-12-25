from tkinter import *
from tkinter import messagebox

from Graph import *

#constants for the window:
WIDTH = 1000
HEIGHT = 600
line = 20

#constants for graph part of the visualization
X_CENTER = WIDTH*2/3
Y_CENTER = HEIGHT/2
R = min(WIDTH, HEIGHT)*0.4

# constants for vertices and edges representations
VERTEX_RADIUS = 15
VERTEX_COLOR = "yellow"
vertexArray = []
edgeArray = []

# constants for labels
VERTEX_LABEL_HEIGHT = 15
VERTEX_LABEL_WIDTH = 12
labelArray = []

#setting up tkinter canvas
root = Tk()
canvas_bg = "aquamarine"
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg = canvas_bg)

generate_button = Button(canvas, text="Generate", command=lambda:onButtonPress())
generate_button.place(x=WIDTH/8, y=HEIGHT/2)

v_entry = Entry(canvas, width=5)
v_entry.place(x=WIDTH/5, y=HEIGHT/10)
e_entry = Entry(canvas, width=5)
e_entry.place(x=WIDTH/5, y=HEIGHT/10+line)

entry_label_vertex = Label(canvas, text = "Number of vertices:", bg = canvas_bg)
entry_label_vertex.place(x=WIDTH/5 - 130, y=HEIGHT/10)
entry_label_edge = Label(canvas, text = "Number of vertices:", bg = canvas_bg)
entry_label_edge.place(x=WIDTH/5 - 130, y=HEIGHT/10+line)

loops = BooleanVar()
loops.set(False)
loops_check = Checkbutton(canvas, text = "allow loops", variable = loops, onvalue="True", offvalue="False", bg = canvas_bg)
loops_check.place(x=WIDTH/5 - 130, y=HEIGHT/10 + line*3)

directed = BooleanVar()
directed.set(False)
directed_check = Checkbutton(canvas, text = "directed", variable = directed, onvalue="True", offvalue="False", bg = canvas_bg)
directed_check.place(x=WIDTH/5 - 130, y=HEIGHT/10 + line*4)

v = IntVar()
e = IntVar()
v.set(2)
e.set(2)

def generate_graph(v, e):
    # generate graph

    if loops.get() == True:
        graph = Graph(v, e, True)
    else:
        graph = Graph(v, e, False)

    if directed.get() == True:
        graph.directed = True
    else:
        graph.directed = False

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

    #draw edges
    for e in graph.edgeArray:
        vertex1_index = ord(e[0]) - 97
        vertex2_index = ord(e[1]) - 97
        x1 = vertexPosArray[vertex1_index][0]
        y1 = vertexPosArray[vertex1_index][1]
        x2 = vertexPosArray[vertex2_index][0]
        y2 = vertexPosArray[vertex2_index][1]
        if graph.directed == True:
            draw_edge(x1, y1, x2, y2, True)
        else:
            draw_edge(x1,y1,x2,y2, False)


    # print vertex set and edge set onto console.
    graph.printGraph()


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
def draw_label(name, x, y, bg, w, h):
    # make a frame to allow customization of label size
    #frame = Frame(canvas, width=w, height=h, bg=bg)
    #frame.place(x=x-w/2, y=y-h/2)
    # make label and pack it on frame.
    var = StringVar()
    label = Label(canvas, textvariable = var, bg = bg)
    label.place(x=x-6, y=y-9)
    labelArray.append(label)
    var.set(name)

# draws vertex centered around x, y coordinates
def draw_vertex(name, x, y, r):
    # draw vertices
    canvas.create_oval(x-r, y-r, x+r, y+r, fill = VERTEX_COLOR)
    # draw labels for the vertices
    draw_label(name, x, y, VERTEX_COLOR, VERTEX_LABEL_WIDTH, VERTEX_LABEL_HEIGHT)

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
        l.place_forget()
    labelArray.clear()

    generate_graph(v.get(), e.get())
    print("button pressed")

canvas.pack()
root.mainloop()