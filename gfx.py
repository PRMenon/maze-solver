from tkinter import Tk, BOTH, Canvas
from time import sleep

class Window:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.__root: Tk = Tk()
        self.__root.title = "Maze Solver"
        self.__canvas: Canvas = Canvas(width=self.width, height=self.height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.is_running: bool = False
        
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def draw_line(self, line: "Line", fill_color: str = "black") -> None:
        line.draw(self.__canvas, fill_color)
    
    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.is_running = True
        while (self.is_running):
            self.redraw()

    def close(self) -> None:
        self.is_running = False


class Point():
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __repr__(self):
        return f"({self.x},{self.y})"


class Line():
    def __init__(self, start: "Point", end: "Point"):
        self.start: Point = start
        self.end: Point = end

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y,
            fill=fill_color, width=2)

    def __repr__(self):
        return f"Line between {self.start} and {self.end}"
    

class Cell():
    def __init__(self, window: "Window"):
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self._x1: int = 0
        self._x2: int = 0
        self._y1: int = 0
        self._y2: int = 0
        self._win = window

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
    
    def _get_midpoint(self) -> "Point":
        return Point(
            abs(self._x1 - self._x2) // 2,
            abs(self._y1 - self._y2) // 2)

    def draw_move(self, to_cell: "Cell", undo=False):   
        fill_color = "gray" if undo else "red"
        line: Line = Line(self._get_midpoint(), to_cell._get_midpoint())
        self._win.draw_line(line, fill_color)

class Maze():
    def __init__(self, x1: int, y1: int,
                 num_rows: int, num_cols: int,
                 cell_size_x: int, cell_size_y: int,
                 win: "Window"):
        self._x1: int = x1
        self._y1: int = y1 
        self._num_rows: int = num_rows
        self._num_cols: int = num_cols
        self._cell_size_x: int = cell_size_x
        self._cell_size_y: int = cell_size_y
        self._win: "Window" = win

        self._cells = []
        self._create_cells()

    def _create_cells(self) -> None:
        dummy_cell: "Cell" = Cell(self._win)
        dummy_col = [dummy_cell] * self._num_rows
        self._cells = [dummy_col] * self._num_cols
        
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cells(i, j)

    def _draw_cells(self, i: int, j: int) -> None:
        x1: int = self._x1 + i * self._cell_size_x
        y1: int = self._y1 + j * self._cell_size_y

        x2: int = x1 + self._cell_size_x
        y2: int = y1 + self._cell_size_y

        current_cell: "Cell" = self._cells[i][j]
        current_cell.draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        self._win.redraw()
        sleep(0.05)

        
