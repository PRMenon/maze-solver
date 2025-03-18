from tkinter import Canvas

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

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y,
            fill=fill_color, width=2)

    def __repr__(self):
        return f"Line between {self.start} and {self.end}"
    
class Cell():
    def __init__(
            self, window, top_left: Point, bottom_right: Point, 
            has_left_wall: bool = True, has_right_wall: bool = True,
            has_top_wall: bool = True, has_bottom_wall: bool = True,
            ):
        
        self._win = window
        self.top_left: Point = top_left
        self.bottom_right: Point = bottom_right
        self.top_right: Point = Point(self.bottom_right.x, self.top_left.y)
        self.bottom_left: Point = Point(self.top_left.x, self.bottom_right.y)

        self.has_left_wall = has_left_wall
        self.has_right_wall= has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall

        self.mid_x = (self.top_left.x + self.top_right.x) // 2
        self.mid_y = (self.top_left.y + self.bottom_left.y) // 2

    def draw(self):
        if self.has_top_wall:
            self._win.draw_line(Line(self.top_left, self.top_right),
                                "black")

        if self.has_bottom_wall:
            self._win.draw_line(Line(self.bottom_left, self.bottom_right),
                                "black")

        if self.has_left_wall:
            self._win.draw_line(Line(self.top_left, self.bottom_left),
                                "black")

        if self.has_right_wall:
            self._win.draw_line(Line(self.top_right, self.bottom_right),
                                "black")

    def draw_move(self, to_cell, undo: bool = False):
        color = "red" if undo else "gray"
        self._win.draw_line(
            Line(Point(self.mid_x, self.mid_y),
                 Point(to_cell.mid_x, to_cell.mid_y)),
                 color)

class Maze():
    ...