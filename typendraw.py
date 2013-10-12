# random circles in Tkinter
# a left mouse double click will idle action for 5 seconds
# modified vegaseat's code from:
# http://www.daniweb.com/software-development/python/code/216626
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class TypeDraw(tk.Canvas):
    """
    A Canvas variant with predefined bindings for typing and drawing.
    """
    def __init__(self, master=None, cnf={}, **kw):
        tk.Canvas.__init__(self, master=master, cnf=cnf, **kw)
        self.mx = -1
        self.my = -1
        # self.background_color = 'white'
        self.draw_color = 'black'
        self.font = ('Consolas', 16)
        self.line_width = 2
        # self.cv = tk.Canvas(self.root, width=self.w, height=self.h, bg='black')
        # self.cv.pack(fill=tk.BOTH)
        self.bind('<Button-1>', self.catch_mouse)
        self.bind_all('<Key>', self.key_pressed) # have to use bind all
        self.bind('<B1-Motion>', self.draw)
        # self.bind('<B3-Motion>', self.draw)

    def catch_mouse(self, event = None):
        self.mx = event.x
        self.my = event.y
        # self.root.update()

    def key_pressed(self, event=None):
        self.create_text(self.mx, self.my, text = event.char, font=self.font, fill=self.draw_color)
        self.mx = self.mx+(self.font[1]-4) # shift after draw a character
        # self.root.update()

    def draw(self, event=None):
        mx = event.x
        my = event.y
        if self.mx >= 0:
            self.create_line(self.mx, self.my, mx, my, width=self.line_width, fill=self.draw_color)
        self.mx=mx
        self.my=my

    def clear(self, event=None):
        self.delete(tk.ALL)

    def change_font(self,font):
        self.font = font
        
    def change_color(self,color):
        self.draw_color = color
    
    def change_linewidth(self,width):
        self.line_width = width