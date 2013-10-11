#!/usr/bin/python
import os
import time
from typendraw import TypeDraw,tk

os.chdir(os.getenv('HOME')) # change dir to the HOME

def save_ps(cv): # wapper to call the canvas postscript saving 
    m_d_hms = time.ctime().split(' ')[1:-1]
    h_m = m_d_hms[2].split(':')[0:-1]
    file_to_save= m_d_hms[0] + m_d_hms[1] + '_' + h_m[0] + 'h' + h_m[1] + '.eps'
    print file_to_save
    return lambda: cv.postscript(file=file_to_save, colormode='color')

root = tk.Tk()
root.geometry("640x480+80+60")
root.title('Type and Draw')
app = TypeDraw(root, bg='white')
app.pack(fill=tk.BOTH, expand=1)

# add save menu
menu = tk.Menu(root, tearoff=0)
# root.config(menu=menu)
menu.add_command(label="Save", command=save_ps(app))
menu.add_separator()
menu.add_command(label="Clear", command=app.clear)

root.bind('<Button-3>', lambda e: menu.post(e.x_root, e.y_root))
root.mainloop()

        

