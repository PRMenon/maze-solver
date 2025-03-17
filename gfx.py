from tkinter import Canvas
import logging

class Point():
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __repr__(self):
        return f"({self.x},{self.y})"

class Line():
    def __init__(self, start: Point, end: Point):
        self.start: Point = start
        self.end: Point = end
        # self.x1 = start.x
        # self.y1 = start.y
        # self.x2 = end.x
        # self.y2 = end.y
        logging.info(self)

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y,
            fill=fill_color, width=2)

    def __repr__(self):
        return f"Line between {self.start} and {self.end}"
    
class Cell():
    ...