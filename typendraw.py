"""
A canvas class with type and draw feature.
Author: Rong Xiao <akelux@gmail.com>
LICENSE: GPL 2.0
"""

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

from font_chooser import askChooseFont

from tkColorChooser import askcolor

import tkFileDialog, tkMessageBox

class TypeDraw(tk.Canvas):
    """
    A Canvas variant with predefined bindings for typing and drawing.
    """
    def __init__(self, master=None, cnf={}, **kw):
        tk.Canvas.__init__(self, master=master, cnf=cnf, **kw)
        self.mx = -1
        self.my = -1
        self.draw_color = 'black'
        self.color = 'white'
        self.font = ('Consolas', 16)
        self.line_width = 2
        self.em = 12

        self.saved = True

        self.cursor = None
        self.blink = False
        self.stack = [] # history for redo

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
        # print 'event.char:', event.char
        # print "key symbol:", event.keysym
        if len(event.char) != 1: # process combined control keys
            sym = event.keysym
            # if sym == 'Escape':
            #    self.blink = False
            if sym == 'Right':
                self.mx += 1
            elif sym == 'Left':
                self.mx -= 1
            elif sym == 'Up':
                self.my -= 1
            elif sym == 'Down':
                self.my += 1
            return

        o = ord(event.char)
        # print "ord:", o
        widget = None
        if o == 32: # don't draw space
            self.mx = self.mx+3*self.em/4
        elif o == 27: # escape
            self.blink = False
        elif o>32 and o<127:
            widget = self.create_text(self.mx, self.my, text = event.char, font=self.font, fill=self.draw_color)
            self.saved = False
            self.stack.append(widget) # put to stack for undo
            self.mx += self.em # shift after draw a character
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
            self.saved = False
            self.stack.append(w)
        self.mx=mx
        self.my=my

    def clear(self, event=None):
        self.delete(tk.ALL)

    def change_color(self,color):
        self.draw_color = color

    def change_linewidth(self,width):
        self.line_width = width

    def blinking(self):
        if self.cursor == None: # draw cursor
            h = 5*self.em/4
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

    def choose_font(self):
        self.font, self.em = askChooseFont(self)

    def set_bgcolor(self):
        self.color = askcolor(parent=self,
                         title='Choose a background color')
        self.config(bg=self.color[1])

    def set_drawcolor(self):
        self.draw_color = askcolor(parent=self,
                         title='Choose a drawing color')[1]

    def save(self):
        if not self.saved:
            f = tkFileDialog.asksaveasfilename(parent=self)
            if f:
                if f[-4:] != '.eps':
                    f+='.eps'
                self.postscript(file=f, colormode='color')
                self.saved = True
        return self.saved

    def load(self): # T.B.D.
        f = tkFileDialog.askopenfilename(parent=self)
        photo = tk.PhotoImage(file=f)
        self.delete(tk.ALL)
        self.create_image(image=photo)

    def close(self): # ask for saving before closing
        if not self.saved:
            ok = tkMessageBox.askyesnocancel(parent=self,
                                             message="Your scratch has unsaved modifications. Do you want to save the scratch?",
                                             title="Save scratch")
            if ok == True:
                return self.save()
            elif ok == None: # cancel
                return False # close without saving
            else: # no
                return True
        return True
