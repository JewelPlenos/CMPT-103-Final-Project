# coordinate_demo.py
# Written by Philip Mees for CMPT 103
# Demonstrating coordinate conversion without the use of the setCoords, toWorld, and toScreen methods,
# and without the need to downgrade to graphics.py version 4.
# This uses lonlat_to_xy coordinate conversion function.

from graphics import *


def main():
    win = GraphWin('ETS Data', 800, 920)
    img = Image(Point(win.getWidth() // 2, win.getHeight() // 2), 'edmonton.png')
    img.draw(win)

    # Draw a circle if pixel coordinates are known.
    circle1 = Circle(Point(400, 460), 100)
    circle1.setOutline('red')
    circle1.setWidth(4)
    circle1.draw(win)

    # Draw a circle if longitude and latitude are known: convert lon, lat to x, y first.
    x, y = lonlat_to_xy(win, -113.5, 53.5)
    circle2 = Circle(Point(x, y), 100)
    circle2.setOutline('green')
    circle2.setWidth(4)
    circle2.draw(win)

    win.getMouse()
    win.close()


def lonlat_to_xy(win, lon, lat):
    '''Written by Philip Mees for CMPT 103
    Purpose: convert longitude/latitude locations to x/y pixel locations
        This avoids the use of the setCoords, toWorld, and toScreen methods and graphics.py incompatibilities
    Parameters:
        win (GraphWin): the GraphWin object of the GUI
        lon, lat (float): longitude and latitude to be converted
    Returns: x, y (int): pixel location inside win'''

    xlow, xhigh = -113.720049, -113.320418
    ylow, yhigh = 53.657116, 53.393703

    width, height = win.getWidth(), win.getHeight()

    x = (lon - xlow) / (xhigh - xlow) * width
    y = (lat - ylow) / (yhigh - ylow) * height

    return int(x), int(y)


if __name__ == '__main__':
    main()
