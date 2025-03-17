from tkinter import Tk, BOTH, Canvas
from gfx import Line
import logging

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = "Maze Solver"
        self.__canvas = Canvas(width=self.width, height=self.height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.is_running = False
        
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def draw_line(self, line:Line, fill_color: str):
        line.draw(self.__canvas, fill_color)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.is_running = True
        while (self.is_running):
            self.redraw()
        logging.info("Closing the window")

    def close(self):
        self.is_running = False

        

