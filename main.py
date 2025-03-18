from window import Window
from gfx import Line, Point, Cell
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the window")
    win = Window(800, 600)
    cell1 = Cell(win, Point(200,300), Point(300, 400), has_right_wall=False)
    cell2 = Cell(win, Point(300,300), Point(400, 400), has_left_wall=False)
    cell1.draw()
    cell2.draw()
    cell1.draw_move(cell2)
    win.wait_for_close()

if __name__ == "__main__":
    main()
