import pickle
from datetime import date
from graphics4 import *

def main() -> None:
    '''
    Purpose: Run the main program loop for Edmonton Transit System interface and handles user input and dispatches commands to appropriate functions.
    Parameters: None
    Return: None
    '''    
    valid = True    
    
    routes = {}
    shapes = {}
    disruptions = []
    
    while True:
        print("""
Edmonton Transit System
------------------------------------
(1) Load route data
(2) Load shapes data
(3) Load disruptions data
        
(4) Print shape IDs for a route
(5) Print coordinates for a shape ID
(6) Find longest shape for route

(7) Save routes and shapes in  a pickle
(8) Load routes and shapes from a pickle
        
(9) Interactive map
(0) Quit
        """)
 
        choice = input("Enter Command: ")
    
        if choice.isdigit():
            choice = int(choice)
            if 0 <= choice <= 9:
                valid = True
            else:
                print("Invalid choice. Please try again!")
        else:
            print("Invalid choice. Please try again!")
        if choice == 0:
            break
        elif choice == 1:
            routes = load_routes('data/routes.txt')
            print()
            
        elif choice == 2:
            shapes = load_shapes()
            
        elif choice == 3:
            disruptions = load_disruptions()
    
        elif choice == 4:
            try:
                print_shape_id(routes)
            except UnboundLocalError as err:
                print(err)
                print("Route data hasn't been loaded yet")
        elif choice == 5:
            try:
                coordinates(shapes)
            except UnboundLocalError as err:
                print(err)
                print("Shape ID data hasn't been loaded yet")  
        elif choice == 6:
            try:
                long_shapes(routes, shapes)
            except UnboundLocalError as err:
                print(err)
                print("Data hasn't been loaded yet")
                
        elif choice == 7:
                filename = input('Enter filename: ')
                save_pickle(filename, routes, shapes, disruptions)
        elif choice == 8:
            filename = input('Enter filename: ')
            routes, shapes, disruptions = load_pickle(filename)
        
        elif choice == 9:
            win, search_button, clear_button, from_entry, to_entry = interface(disruptions)
            draw_route(win, search_button, clear_button, from_entry, to_entry, routes, shapes)

def load_routes(filename1: str) -> dict:
    '''
    Purpose: Load route and trip data from files to create route metadata and associated shape IDs.
    Parameters: filename1 (str): Path to routes.txt file containing route information
    Return: tuple: Contains two elements:
            - route_names (dict): Dictionary mapping route IDs to route names
            - routes (dict): Nested dictionary with route IDs as keys, containing route names and associated shape IDs
    '''    
    try:
        route_names = index_routes(filename1) # create 1st data structure required (dictionary) in helper function
        
        routes = {} # create 2nd data structure (dictionary) 
        #{routes:  {routename:{shape id} {route id}}
        for route_id, name in route_names.items():
            routes[route_id] = {'route_name': name.strip('"'), 'shape_ids': set()}
        
        # ask user for trips filename with default
        filename2 = input("Enter a filename: ").strip()
        
        if not filename2:
            filename2 = "data/trips.txt"
            
        routes = compile_routes(filename2, routes) # index through trips.txt and combine data structures into routes dict in helper function
        
        print(f'Data from {filename2} loaded')
        print(routes)
        return routes
        
    except FileNotFoundError as err:
        return err

def index_routes(filename1):
    
    route_names = {}
    
    with open(filename1) as f1:
        next(f1)  # Skip header
        for line in f1: # index through the file stripping and splitting while collecting the route id and name, saving it in a cictionary
            parts = line.strip().split(',')
            route_id = parts[0]
            route_name = parts[3]
            route_names[route_id] = route_name
            
    return route_names

def compile_routes(filename2, routes):
    
    # {routes:  {routename:{shape id} {route id}}
    
    with open(filename2) as f2:
        next(f2)  # skip header
        for line in f2: # index through file and splitting while collecting route id and shape id
            parts = line.strip().split(',') # same process but for the second file
            route_id = parts[0]
            shape_id = parts[6]
            if route_id in routes:
                routes[route_id]['shape_ids'].add(shape_id) # add the shape ids
    return routes    

def load_shapes() -> dict:
    '''
    Purpose: Load geographic coordinate data for transit shapes from a file.
    Parameters: None 
    Return: dict: Dictionary mapping shape IDs to lists of (latitude, longitude) coordinate tuples
    '''
    
    shapes = {} # create shapes data structure
    try:
        filename = input("Enter a filename: ").strip()
        if not filename:
            filename = "data/shapes.txt"
        with open(filename) as f:# index through 'shapes.txt' collecting shape_ids, long, and lat
            next(f) # skip header
            for line in f:
                shape_id = line.strip().split(',')[0]
                shape_pt_lat = line.strip().split(',')[1]
                shape_pt_lon = line.strip().split(',')[2]
                coord = float(shape_pt_lat), float(shape_pt_lon)
                if not shape_id in shapes:
                    coords = []
                    shapes[shape_id] = coords
                else:
                    coords.append(coord)    
    except FileNotFoundError as err: # error check if the file doesnt exist
        print(err)
    
    print(f'Data from {filename} loaded')
    return shapes

def load_disruptions():
    '''
    purpose: index through filename and add longitude and latitude of disruptions still ongoing
    parameters: filename
    return: disruptions
    '''
    filename = input("Enter a filename: ").strip()
    if not filename:
        filename = "data/traffic_disruptions.txt" 
    
    disruptions = [] # [(lon, lat)]
    
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    
    try:
        with open(filename) as file:
            file.readline() * 2
            for line in file:
                disr_date_first, disr_date_year = line.strip().split(',')[5] , line.strip().split(',')[6]
                disr_date_first, disr_date_year = disr_date_first.strip(), disr_date_year.strip()
                disr_date_first, disr_date_year = disr_date_first.strip('"'), disr_date_year.strip('"')
                
                disr_date_month, disr_date_day = disr_date_first.split()[0], disr_date_first.split()[1]
                
                if disr_date_month in months:
                    disr_date_month = months[disr_date_month]
                disr_date = date(int(disr_date_year), disr_date_month, int(disr_date_day))
                if disr_date > date.today():
                    point = line.strip().split(',')[-1]
                    lon, lat = float(point.strip('POINT ()').split(' ')[0]), float(point.strip('POINT ()').split(' ')[1])
                    disrupt = lon, lat
                    disruptions.append(disrupt)
        print(f'Data from {filename} loaded')
        return disruptions
                
    except FileNotFoundError as err:
        print(err)

#{routes:  {routename:{shape id} {route id}}
def print_shape_id(routes: dict) -> None:
    route_id = input('Enter route: ')
    
    if route_id in routes:
        print(f"Shape ids for route [{routes[route_id]['route_name']}]")        
        for shape_id in routes[route_id]['shape_ids']:
            print(f'\t{shape_id}')
    else:
        print('\t**NOT FOUND**')

def coordinates(shapes: dict) -> None:
    '''
    Purpose: Print all geographic coordinates associated with a specific shape ID.
    Parameters: shapes (dict): Dictionary of shape data (from load_shapes()) to search
    Return: None (prints results directly to console)
    '''    
    shape_id = input("Enter shape ID: ") # ask user for an id
    if shape_id in shapes: # check if the id is in shapes
        print(f'Shape ID coordinates for {shape_id}')
        for coord in shapes[shape_id]: # print out all the coordinates for that id 
            print(f'\t{coord}')
    else:
        print("\t**NOT FOUND**")
        
#{routes:  {routename:{shape id} {route id}}        
def long_shapes(routes, shapes):
    
    route_id = input("Enter route ID: ")
    shape_ids = routes[route_id]['shape_ids']
    max_length = -1
    longest_shape = None 
    for shape_id in shape_ids:  
        if shape_id in shapes:
            current_length = len(shapes[shape_id])
            if current_length > max_length:
                max_length = current_length
                longest_shape = shape_id
    if longest_shape:
        print(f"The longest shape for route {route_id} is {longest_shape} with {max_length} points.")
    return longest_shape
      
def save_pickle(filename, routes, shapes, disruptions):
    if filename == '':
        filename = 'data/etsdata.p'    
    
    try:
        with open(filename, 'wb') as file:
                pickle.dump((routes, shapes, disruptions), file)
        print('Data structures successfully written to data/etsdata.p')
    except UnboundLocalError as err:
        with open(filename, 'wb') as file:
                pickle.dump((routes, shapes, disruptions), file)
        print('Data structures successfully written to data/etsdata.p') 
    
def load_pickle(filename):
    if filename == '':
        filename = 'data/etsdata.p'
    try:
        with open(filename,'rb') as file:
                routes, shapes, disruptions = pickle.load(file)
        print('Routes and shapes Data structures successfully loaded from data/etsdata.p')
        return routes, shapes, disruptions
    except FileNotFoundError as err:
        print(err)

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

def interface(disruptions):
    
    win = GraphWin('ETS Data', 800, 920)
    image_canvas = Rectangle(Point( 0,0 ), Point( 800 ,920 )) 
    image_canvas.draw(win)    
    map_of_edmonton = load(image_canvas.getCenter(), win, disruptions) 
    from_text = Text(Point(70, 50), 15)
    from_text.setText('From:')
    from_text.setStyle('bold')
    from_text.draw(win)
    
    to_text = Text(Point(70, 85), 15)
    to_text.setText('To:')
    to_text.setStyle('bold')
    to_text.draw(win)            

    from_entry = Entry(Point(170, 50), 15) # Test entry box
    from_entry.setText('')
    from_entry.draw(win)
    
    to_entry = Entry(Point(170, 85), 15)
    to_entry.setText('')
    to_entry.draw(win)
    
    search_button = Rectangle(Point(105, 105), Point(240, 130))
    search_button.setFill('#FB8C00')
    search_button.setOutline('black')
    search_text = Text(search_button.getCenter(), 'Search')
    search_text.setSize(15)
    search_text.setStyle('bold')
    search_button.setWidth(2)
    search_button.draw(win)
    search_text.draw(win)
    
    clear_button = Rectangle(Point(105, 135), Point(240, 160))
    clear_button.setFill('#FB8C00')
    clear_button.setOutline('black')
    clear_button.setWidth(2)
    clear_text = Text(clear_button.getCenter(), 'Clear')
    clear_text.setSize(15)
    clear_text.setStyle('bold')            
    clear_button.draw(win)          
    clear_text.draw(win)
    
    click_point = win.getMouse()

    
    return win, search_button, clear_button, from_entry, to_entry


def draw_route(win, search_button, clear_button, from_entry, to_entry, routes, shapes): 
    
    while True:
        try:
            click_point = win.getMouse()  # get click coordinates
            if in_rectangle(click_point, search_button):  # handle search button click
                start = from_entry.getText().strip()
                end = to_entry.getText().strip()                
                
                if start and end:  # 1st case search (both start and end)
                    for route_id in routes: # find route matching both start and end points
                        long_name = routes[route_id]['route_name'].split(' - ')
                        if (start in long_name) and (end in long_name):
                            print(long_name)
                            temp = route_id
                            break
                else:  # 2nd case search (either start or end)
                    for route_id in routes:  # find routes matching either location
                        long_name = routes[route_id]['route_name'].split(' - ')
                        if (start in long_name) or (end in long_name):
                            temp = route_id                            
                            print(temp)
                            
    
                shape_ids = routes[temp]['shape_ids']
                for shape_id in shape_ids:
                    if shape_id not in shapes: # check if the shape id is valid
                        continue  
                        
                    # get coordinates for this shape_id
                    shape_coords = shapes[shape_id]
                    
                    converted_points = []
                    for coord in shape_coords:
                        lat, lon = coord
                        x, y = lonlat_to_xy(win, lon, lat)
                        converted_points.append((x, y))
                    
                    # draw line for this route segment
                    if len(converted_points) >= 2:
                        prev_point = converted_points[0]
                        for point in converted_points[1:]:
                            # connect 1st point to 2nd point
                            line = Line(Point(*prev_point), Point(*point))
                            line.setOutline('blue')
                            line.setWidth(2)
                            line.draw(win)
                            prev_point = point
                
            if in_rectangle(click_point, clear_button):  # Handle clear button click
                # Reset input fields
                from_entry.setText('')
                to_entry.setText('')                        
                        
        except GraphicsError:
            break    
        
def in_rectangle(click_point, rect) -> bool:
    '''
    Purpose: Check if point is contained within rectangle
    Parameters: click_point (Point) -> Click location to check. rect (Rectangle) -> Rectangle object to check against
    Return: is_inside (bool) -> True if point is within rectangle
    '''    
    p1 = rect.getP1()
    p2 = rect.getP2()
    return (min(p1.getX(), p2.getX()) <= click_point.getX() <= max(p1.getX(), p2.getX()) and min(p1.getY(), p2.getY()) <= click_point.getY() <= max(p1.getY(), p2.getY()))
    
    
def load(anchor_point, win, disruptions):
    '''
    Purpose: Load an image file into the application window  
    Parameters: anchor_point (Point) -> Center position for image display win (GraphWin) -> Window to display the image in
    Return: image (Image/None) -> Loaded image object or None if canceled
    '''    
    
    map_of_edmonton = Image(anchor_point, 'edmonton.png')
    map_of_edmonton.draw(win)
    
    for index in range(len(disruptions)): # convert longitude and latitude into python graphics x y coordinates
        lon = disruptions[index][0]
        lat = disruptions[index][1]
        x , y = lonlat_to_xy(win, lon, lat)
            
        spot = Circle(Point(x,y), 3) # plot disruptions on map
        spot.setFill('red')
        spot.setOutline('red')
        spot.draw(win)    
    
    return map_of_edmonton  

main()
