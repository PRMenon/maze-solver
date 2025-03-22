from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

class Window:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.__root: Tk = Tk()
        self.__root.title = "Maze Solver"
        self.__canvas: Canvas = Canvas(width=self.width, height=self.height, background="white")
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
    def __init__(self, window: "Window" = None):
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self._x1: int = 0
        self._x2: int = 0
        self._y1: int = 0
        self._y2: int = 0
        self._win = window
        self._visited = False

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        
        if not self._win:
            return
        
        line_color_l: str = "black" if self.has_left_wall else "white"
        line_color_t: str = "black" if self.has_top_wall else "white"
        line_color_r: str = "black" if self.has_right_wall else "white"
        line_color_b: str = "black" if self.has_bottom_wall else "white"
        
        self._win.draw_line(Line(Point(x1, y1), Point(x1, y2)), line_color_l)
        self._win.draw_line(Line(Point(x1, y1), Point(x2, y1)), line_color_t)
        self._win.draw_line(Line(Point(x2, y1), Point(x2, y2)), line_color_r)
        self._win.draw_line(Line(Point(x1, y2), Point(x2, y2)), line_color_b)
        
    def _get_midpoint(self) -> "Point":
        midpoint = Point(
            self._x1 + abs(self._x1 - self._x2) // 2,
            self._y1 + abs(self._y1 - self._y2) // 2)
        return midpoint

    def draw_move(self, to_cell: "Cell", undo=False):
        if not self._win:
            return   
        
        fill_color = "gray" if undo else "red"
        line: Line = Line(self._get_midpoint(), to_cell._get_midpoint())
        self._win.draw_line(line, fill_color)

class Maze():
    def __init__(self, x1: int, y1: int,
                 num_rows: int, num_cols: int,
                 cell_size_x: int, cell_size_y: int,
                 win: "Window" = None, seed:int = None):
        self._x1: int = x1
        self._y1: int = y1 
        self._num_rows: int = num_rows
        self._num_cols: int = num_cols
        self._cell_size_x: int = cell_size_x
        self._cell_size_y: int = cell_size_y
        self._win: "Window" = win

        if seed:
            random.seed(seed)

        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_visited()

    def _create_cells(self) -> None:
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                column.append(Cell(self._win))
            self._cells.append(column)
        
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

    def _break_entrance_and_exit(self) -> None:
        self._cells[0][0].has_top_wall = False
        self._draw_cells(0,0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cells(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i: int, j: int) -> None:
        current_cell: "Cell" = self._cells[i][j]
        current_cell._visited = True
        
        while (True):
            to_visit = []
            
            t: tuple = (i, j - 1)
            b: tuple = (i, j + 1)
            l: tuple = (i - 1, j)
            r: tuple = (i + 1, j)

            if j > 0 and not self._cells[i][j - 1]._visited:
                to_visit.append(t)
            if j < self._num_rows - 1 and not self._cells[i][j + 1]._visited:
                to_visit.append(b)
            if i > 0 and not self._cells[i - 1][j]._visited:
                to_visit.append(l)
            if i < self._num_cols - 1 and not self._cells[i + 1][j]._visited:
                to_visit.append(r)
            
            if len(to_visit) == 0:
                self._draw_cells(i, j) 
                return

            direction: tuple = to_visit[random.randrange(len(to_visit))]

            if direction == l:
                current_cell.has_left_wall = False
                self._cells[direction[0]][direction[1]].has_right_wall = False
            if direction == r:
                current_cell.has_right_wall = False
                self._cells[direction[0]][direction[1]].has_left_wall = False
            if direction == t:
                current_cell.has_top_wall = False
                self._cells[direction[0]][direction[1]].has_bottom_wall = False
            if direction == b:
                current_cell.has_bottom_wall = False
                self._cells[direction[0]][direction[1]].has_top_wall = False
            
            self._break_walls_r(*direction)

    def _reset_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):                
                self._cells[i][j]._visited = False

    def solve(self):
        self._solve_r(0, 0)
    
    def _solve_r(self, i: int, j: int) -> bool:
        self._animate()
        current_cell: "Cell" = self._cells[i][j]
        current_cell._visited = True
        
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        if (j > 0 
            and not self._cells[i][j - 1]._visited 
            and not current_cell.has_top_wall
            ):
            current_cell.draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            current_cell.draw_move(self._cells[i][j - 1], True)
        if (j < self._num_rows - 1 
            and not self._cells[i][j + 1]._visited 
            and not current_cell.has_bottom_wall
            ):
            current_cell.draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            current_cell.draw_move(self._cells[i][j + 1], True)
        if (i > 0 
            and not self._cells[i - 1][j]._visited 
            and not current_cell.has_left_wall
            ):
            current_cell.draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            current_cell.draw_move(self._cells[i - 1][j], True)
        if (i < self._num_cols - 1 
            and not self._cells[i + 1][j]._visited 
            and not current_cell.has_right_wall
            ):
            current_cell.draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            current_cell.draw_move(self._cells[i + 1][j], True)
        
        return False
    
    def _animate(self):
        if not self._win:
            return
        self._win.redraw()
        sleep(0.05)

        
