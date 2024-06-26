from tkinter import *
from tkinter import messagebox

def create_circle(center, radius, fill='', outline='', width=1):
    x, y = center
    C.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill, outline=outline,width=width)

top = Tk()
C = Canvas(top, bg="grey18", height=500, width=500)
C.create_rectangle(100, 50, 400, 450, fill="grey29", outline="white")
center_y = 100
C.create_oval(200, 50+center_y, 300, 150+center_y)
C.create_rectangle(200, 50, 300, 150+center_y/2)
minus = 50
x_minus = 30
C.create_arc((100+x_minus, 50+minus, 400-x_minus, 250+minus), start=0, extent=-180, style=ARC)
C.create_line(100+x_minus, 50, 100+x_minus, 200)
C.create_line(400-x_minus, 50, 400-x_minus, 200)
C.create_rectangle(250-40, 50, 250+40, 60, fill="white", outline="gray")
create_circle((250, 75), 15, outline="orange red", width=5)


C.pack()
top.mainloop()

