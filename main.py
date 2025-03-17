from window import Window
from gfx import Line, Point
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the window")
    win = Window(800, 600)
    line1 = Line(Point(100, 200), Point(200, 200))
    line2 = Line(Point(200, 300), Point(300, 400))
    win.draw_line(line1, "red")
    win.draw_line(line2, "black")
    win.wait_for_close()

if __name__ == "__main__":
    main()
