# lonlat_to_xy.py
# Written by Philip Mees for CMPT 103


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
