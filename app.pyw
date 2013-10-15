#!/usr/bin/python
"""
Author: Rong Xiao <akelux@gmail.com>
LICENSE: GPL 2.0
"""
import os
import time
from typendraw import TypeDraw,tk
import Tix

#root window
root = Tix.Tk()
# root = tk.Tk()
root.geometry("640x480+80+60")
root.title('Type and Draw')

#canvas initialization
app = TypeDraw(root, bg='white')
app.pack(fill=tk.BOTH, expand=1)

# add menu for save and clear
menu = tk.Menu(root, tearoff=0)

#change color menu
color_menu = tk.Menu(menu, tearoff=0)
color_menu.add_command(label="Drawing", command=app.set_drawcolor)
color_menu.add_command(label="Background", command=app.set_bgcolor)
menu.add_cascade(label="Change color", menu=color_menu)

#change line_with menu
linewidth_menu = tk.Menu(menu, tearoff=0)

for w in range(1,9): # change here to have more options
    linewidth_menu.add_command(label=str(w) + ' px', command=lambda:app.change_linewidth(w))

menu.add_cascade(label="Change line width", menu=linewidth_menu)

#change font menu
menu.add_command(label="Change font", command=app.choose_font)


#other menu items: save, clear, quit
menu.add_separator()
menu.add_command(label="Save", command=app.save)
# menu.add_command(label="Load", command=app.load)
menu.add_command(label="Clear", command=app.clear)
menu.add_command(label="Quit", command=lambda: root.quit()) 

app.bind('<Enter>', lambda e: menu.unpost()) # Fixing a bug on gtk, the menu is not hiden by itself

# pop menu bindings:
root.bind('<Button-3>', lambda e: menu.post(e.x_root, e.y_root))
root.bind('<Button-2>', lambda e: menu.post(e.x_root, e.y_root))

root.mainloop()
