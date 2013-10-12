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

        self.cursor = None
        self.blink = False
        self.stack = [] # history for redo

        # self.cv = tk.Canvas(self.root, width=self.w, height=self.h, bg='black')
        # self.cv.pack(fill=tk.BOTH)
        self.bind('<Button-1>', self.catch_mouse)
        self.bind_all('<Key>', self.key_pressed) # have to use bind all
        self.bind('<B1-Motion>', self.draw)
        # self.bind('<B3-Motion>', self.draw)
        

    def catch_mouse(self, event = None):
        self.mx = event.x
        self.my = event.y
        self.start_blinking()

        # self.root.update()

    def key_pressed(self, event=None):
        if len(event.char) != 1:
            return
        o = ord(event.char)
        widget = None
        if o == 32: # don't draw space
            self.mx = self.mx+(self.font[1]-4)
        elif o>32 and o<127:
            widget = self.create_text(self.mx, self.my, text = event.char, font=self.font, fill=self.draw_color)
            self.stack.append(widget) # put to stack for undo
            self.mx = self.mx+(self.font[1]-4) # shift after draw a character
            self.start_blinking()
           
        elif o == 127 or o == 8:
            self.blink = False
            if self.stack:
                widget = self.stack.pop()
                self.delete(widget)
        # self.root.update()

    def draw(self, event=None):
        # self.stop_blinking()
        self.blink = False
        mx = event.x
        my = event.y
        if self.mx >= 0:
            w = self.create_line(self.mx, self.my, mx, my, width=self.line_width, fill=self.draw_color)
            self.stack.append(w)
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

    def blinking(self):
        if self.cursor == None: # draw cursor
            h = self.font[1]
            w = (self.line_width+1)/2
            self.cursor = self.create_rectangle(self.mx-w, self.my-h/2, self.mx + w,self.my + h/2,outline = self.draw_color, fill=self.draw_color)
        else: # hide cursor
            self.delete(self.cursor)
            self.cursor = None
        
        if self.blink:    
            self.after(500, self.blinking)
        elif self.cursor:
            self.delete(self.cursor)
            self.cursor = None
     
    def start_blinking(self):
        if not self.blink:
            self.blink = True
            self.after(500, self.blinking)

    """
    def stop_blinking(self):
        if self.blink:
            self.blink = False
            if self.cursor:
                self.delete(self.cursor)
                self.cursor = None
    """      
    
    """
    def set_bg(self, color):
        self.config(bg=color)
    """             