#!/usr/bin/python
import os
import time
from typendraw import TypeDraw,tk
import Tix

os.chdir(os.getenv('HOME')) # change dir to the HOME

def save_ps(cv): # wapper to call the canvas postscript saving 
    m_d_hms = time.ctime().split(' ')[1:-1]
    h_m = m_d_hms[2].split(':')[0:-1]
    file_to_save= m_d_hms[0] + m_d_hms[1] + '_' + h_m[0] + 'h' + h_m[1] + '.eps'
    return lambda: cv.postscript(file=file_to_save, colormode='color')

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
# color_menu.add_command(label="Black", command=lambda:app.change_color('black'))
# color_menu.add_command(label="Yellow", command=lambda:app.change_color('yellow'))
# color_menu.add_command(label="blue", command=lambda:app.change_color('blue'))
color_menu.add_command(label="Drawing", command=app.set_drawcolor)
color_menu.add_command(label="Background", command=app.set_bgcolor)
# menu.add_separator()
menu.add_cascade(label="Change color", menu=color_menu)

#change line_with menu
linewidth_menu = tk.Menu(menu, tearoff=0)
linewidth_menu.add_command(label="1", command=lambda:app.change_linewidth(1))
linewidth_menu.add_command(label="2", command=lambda:app.change_linewidth(2))
linewidth_menu.add_command(label="3", command=lambda:app.change_linewidth(3))
linewidth_menu.add_command(label="4", command=lambda:app.change_linewidth(4))
linewidth_menu.add_command(label="5", command=lambda:app.change_linewidth(5))

menu.add_cascade(label="Change line width", menu=linewidth_menu)

#change font menu
# font_menu = tk.Menu(menu, tearoff=0)
# font_name_menu = tk.Menu(font_menu, tearoff=0)
# font_face_menu = tk.Menu(font_menu, tearoff=0)
# font_size_menu = tk.Menu(font_menu, tearoff=0)
# font_name_menu.add_command(label="Courier New", command=lambda:app.change_fontname('Courier New'))
# font_name_menu.add_command(label="Lucida Console", command=lambda:app.change_fontname('Lucida Console'))
# font_name_menu.add_command(label="Consolas", command=lambda:app.change_fontname('Consolas'))

# font_menu.add_cascade(label="font name", menu=font_name_menu)
# font_menu.add_cascade(label="font size", menu=font_size_menu)
# font_menu.add_cascade(label="font face", menu=font_face_menu)
# menu.add_cascade(label="Change font", menu=font_menu)

#change font menu
# bg_menu = tk.Menu(menu, tearoff=0)
# bg_menu.add_command(label='black', command=lambda: app.config(bg='black'))
# bg_menu.add_command(label='grey', command=lambda: app.config(bg='grey'))
# bg_menu.add_command(label='white', command=lambda: app.config(bg='white'))

menu.add_command(label="Change font", command=app.choose_font)
# menu.add_cascade(label="Change background", menu=bg_menu)

#
menu.add_separator()
menu.add_command(label="Save", command=save_ps(app))
menu.add_command(label="Clear", command=app.clear)
menu.add_command(label="Quit", command=lambda: root.quit()) 
# menu.add_command(label="Dismiss") 
# menu.bind('<Leave>', lambda e: menu.unpost()) # Fixing a bug on gtk, the menu is not hiden by itself
app.bind('<Enter>', lambda e: menu.unpost()) # Fixing a bug on gtk, the menu is not hiden by itself
# pop menu bindings
# root.bind('<Leave>', lambda e: menu.unpost()) # Fixing a bug on gtk, the menu is not hiden by itself
# pop menu bindings
root.bind('<Button-3>', lambda e: menu.post(e.x_root, e.y_root))
root.bind('<Button-2>', lambda e: menu.post(e.x_root, e.y_root))

root.mainloop()
