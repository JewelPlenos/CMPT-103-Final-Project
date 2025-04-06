# ------------------------------- # 
# Group members: Jewel Plenos, Tommy Tran 
# Programming Project - Milestone#1
# ------------------------------- #

from datetime import date
from graphics4 import *

# Load route data
def load_route(routefilename, tripsfilename) -> dict:
    '''
    Purpose: Read the data in routes.txt and trips.txt and store them in appropriate data structures 
    Parameters: routes.txt and trips.txt -> files
    Return: dictionary{route_ids: } 
    '''

    route_dict = {}
    with open(routefilename, 'r') as file: 
        for line in file: 
            parts = line.split(',') 
            if parts[0] == "route_id":
                continue  # skips first row
            route_dict[parts[0]] = parts[3]

    routes = {}
    with open(tripsfilename, 'r') as trips_file:
        for line in trips_file:
            parts = line.strip().split(',')
            if parts[0] == "route_id":
                continue  # skips first row
            route_id = parts[0]
            shape_id = parts[6]
            if route_id not in routes: # initialize route_id key, value if its not already in there 
                routes[route_id] = {
                    'route_name': route_dict.get(route_id, None),
                    'shape_ids': set() 
                }
            routes[route_id]['shape_ids'].add(shape_id) # adds on to already existing route_id key
    return routes
         

# Load shapes data
def load_shapes(filename) -> dict:
    '''
    Purpose: Read the data in shapes.txt 
    Parameters: 'shapes.txt' filename
    Return: dictionary of lon/lat corresponding to their respective shape_id
    '''
    shapes_data_dict = {} 
    with open(filename, 'r') as file: 
        for line in file: 
            coords = [] # Initialize list to store lat, lon 
            parts = line.split(',')
            if parts[0] == 'shape_id': 
                continue # skip row 1 
            shapes_id, lat, lon = parts[0:3] #unpack parts into the needed variables
            coords.append(lat)
            coords.append(lon)
            if shapes_id not in shapes_data_dict:
                shapes_data_dict[shapes_id] = []
            shapes_data_dict[shapes_id] += [coords] # Each individual coord (lat,lon) is added as a list to its respective shapes_id
    return shapes_data_dict


def load_disruption(filename):
    month2number = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    date_location = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split(',')
            if parts[0] == "Disruption ID":
                continue  # skips first row
            finish_date = parts[5].lstrip('"') + parts[6].strip('"') # --> 'Sep 30 2026'
            lst = finish_date.split(' ') # --> ['Sep', '30', '2026']
            date_object = date(int(lst[2]), month2number[lst[0]], int(lst[1])) # --> date(year, month, day) = 2026-09-30
            location = parts[-1] # --> 'POINT (-113.58983573962888 53.425074385191095)'
            coords = location.split(' ')
            lon, lat = float(coords[1].lstrip('(')), float(coords[2].strip('\n').replace(')', '')) # unpack, change to float and remove extra characters 
            date_location[date_object] = lat, lon # --> {2026-09-30: 53.425074385191095, -113.58983573962888}
    return date_location

def input1(): # Helper function for input == 1
    '''
    Purpose: Use user input to run the helper function load_route. -> passes user input as a parameter in load_route
    Parameter: None
    Return: Error message or route_data
    '''
    input_file = input('Enter a filename: ').strip()
    try: 
        if input_file == '':
            input_file = 'data/trips.txt'
        route_data = load_route(f'data/routes.txt', f'{input_file}') # Utilizes load_route helper function 
        print(f'Data from {input_file} loaded')
        return route_data 

    except TypeError: 
        return print(f"IO Error: couldn't open {input_file}")
    except IOError as fail: 
        return print(f"IO Error: couldn't open {input_file}")
    except IndexError: # Index error happens when you try to input shapes.txt instead of trips.txt
        return print(f"IO Error: couldn't open {input_file}")

    

def input2(): # Helper function for input == 2 
    '''
    Purpose: Get user input on which filename to run, utilize helper function load_shapes that saves data from filename to a dictionary
    Parameter: None
    Return: Error message or data from shapes.txt
    '''
    input_shapes = input('Enter a filename: ').strip()
    try: 
        if input_shapes == '':
            input_shapes = 'data/shapes.txt'
        shapes_data = load_shapes(f'{input_shapes}') # Utilizes load_shapes helper function
        print(f"Data from {input_shapes} loaded")
        return shapes_data
    except TypeError: 
        return print(f"IO Error: couldn't open {input_shapes}")
    except IOError as fail: 
        return print(f"IO Error: couldn't open {input_shapes}")    
    except IndexError: # Index error happens when you try to input trips.txt instead of shapes.txt
        return print(f"IO Error: couldn't open {input_shapes}")


def input3() -> dict: # Helper function when input == 3
    '''
    Purpose: Calls load_disruption when input = 3, saves date of disruption and its corresponding coordinate
    Parameter: None
    Return: Dictionary of disruptions and locations
    '''
    input_file = input('Enter a filename: ').strip()
    try: 
        if input_file == '':
            input_file = 'data/traffic_disruptions.txt'
        disruption_data = load_disruption(input_file) # Utilizes load_disruption helper function 
        print(f'Data from {input_file} loaded')
        return disruption_data

    except TypeError: 
        return print(f"IO Error: couldn't open {input_file}")
    except IOError as fail: 
        return print(f"IO Error: couldn't open {input_file}")
    except IndexError: 
        return print(f"IO Error: couldn't open {input_file}")


def print_shape_id(route_data): # Helper function when input == 4 
    '''
    Purpose: Gets user input on specific route number and prints each corresponding shape_id tied to that route
    Parameter: route_data -> stores {"route #": {"route_name": "Abbottsfield - Downtown - University", "shape_ids": {"008-210-South", "xxx"...}}}
    Return: Error message or print shape id
    '''
    input_route = input("Enter route: ").strip()
    try:
        print(f'Shape ids for route [{route_data[input_route]['route_name']}]')
        for item in route_data[input_route]['shape_ids']: 
            print(f'\t {item}')
        print()
    except KeyError:
        return print('\t** NOT FOUND **')
    
def print_coords(shapes_data): # Helper function when input == 5 
    '''
    Purpose: Gets user input on specific shape id, prints every corresponding coordinate 
    Parameter: shapes_data --> stores {shape id: [[lat, lon]]} each lat lon is stored in its own list within the list of all lat, lons -> saved in order
    Return: Error message or prints coords
    '''
    input_id = input("Enter shape ID: ").strip()

    try:
        print(f'Shape id coordinates for {input_id} are:')
        for item in shapes_data[input_id]: 
            print(f'\t({item[0]}, {item[1]})')
        print()
    except KeyError:
        return print('\t** NOT FOUND **')

def input6(route_data, shapes_data): # Helper function when input == 6
    input_route = input('Enter route ID: ').strip()
    current_length = 0
    length_longest = 0
    shape_longest = 0
    try:
        for item in route_data[input_route]['shape_ids']: 
            for coords in shapes_data[item]:
                current_length = len(shapes_data[item])
                if current_length > length_longest: 
                    length_longest = current_length
                    shape_longest = item # item is shape id
        print(f'\nThe longest shape for {input_route} is {shape_longest} with {length_longest} coordinates')
    except KeyError:
        return print('\t** NOT FOUND **')

def input7(route_data, shapes_data, disruption_data): # Helper function when input ==  7
    '''
    Purpose: Save routes and shapes into a pickle file
    Parameter: route_data, dict containing route data
    shapes_data, dict containing shapes data
    Return: None
    '''
    import pickle
    filename = input("Enter a filename: ").strip()
    if filename == "":  # If filename empty use default name
        filename = "data/etsdata.p"
    
    try:  
        with open(filename, 'wb') as f:  # Write to file in binary
            pickle.dump({"route_data": route_data, "shapes_data": shapes_data, "disruption_data": disruption_data}, f)  # Serialize and save dict
        print(f"Data structures successfully written to {filename}")
    except Exception as e:  # Return error if any issues arise
        print(f"Error writing to file: {e}")
 
def input8(): # Helper function when input == 8
    # Load routes and shapes from a pickle
    '''
    Purpose: Load routes and shapes from a pickle file
    Parameter: None
    Return: Tuple containing route and shapes data
    '''
    import pickle
    
    filename = input("Enter a filename: ").strip()  # Prompt user for filename
    if filename == "":
        filename = "data/etsdata.p"
        
    try:  # Attempt to open pickle file and read binary
        with open(filename, 'rb') as f:
            loaded_data = pickle.load(f)
        
        # Inform success    
        print(f"Data successfully loaded from {filename}")
        
        # Retrieve route and shapes from dict and if not present default to empty dict
        route_data = loaded_data.get("route_data", {})
        shapes_data = loaded_data.get("shapes_data", {})
        disruption_data = loaded_data.get("disruption_data", {})
         # Return as tuple
        return route_data, shapes_data, disruption_data
    
    except Exception as e:  #  If file not found or invalid filename display error
        print(f"Error reading from file: {e}")
        
        return {}, {}  # Return empty dictionaries so program doesn't crash
    

def graphical_interface(): # Helper function for input9
    '''
    Purpose: Lay out the gui and background
    Parameter: None
    Return: the GraphWin obj and all the buttons
    '''    
    win_width = 800  # Create win
    win_height = 920
    win = GraphWin("ETS Data", win_width, win_height)
 
    # Center and draw the background img
    bg_image = Image(Point(win_width / 2, win_height / 2), "edmonton.png")
    bg_image.draw(win)
 
    # Create ui elements
    from_text = Text(Point(25, 35), "From:")
    from_text.setStyle("bold")
    from_text.draw(win)
    from_entry = Entry(Point(100, 35), 15)
    from_entry.draw(win)
    from_entry.setFill("white")
 
    # To text and entry
    to_text = Text(Point(32, 65), "To:")
    to_text.setStyle("bold")
    to_text.draw(win)
    to_entry = Entry(Point(100, 65), 15)
    to_entry.draw(win)
    to_entry.setFill("white")
 
    # Search Button
    search_button = Rectangle(Point(42, 90), Point(130, 110))
    search_button.setFill("peru")
    search_button.draw(win)
    search_button.setWidth(3)
    search_text = Text(search_button.getCenter(), "Search")
    search_text.setStyle("bold")
    search_text.draw(win)
 
    # Clear button
    clear_button = Rectangle(Point(42, 115), Point(130, 135))
    clear_button.setFill("peru")
    clear_button.draw(win)
    clear_button.setWidth(3)
    clear_text = Text(clear_button.getCenter(), "Clear")
    clear_text.setStyle("bold")
    clear_text.draw(win)    
    
    click_coord = win.getMouse()  # Obtain coordinate of mouse click
    
    return win, search_button, clear_button, from_entry, to_entry


    
    

def input9(route_data, shapes_data, disruption_data): # Helper function when input == 9
    graphical_interface()
    


# Main 
def main(): 
    quit = False 
    while not quit:
        print("""
Edmonton Transit System
------------------------------------
(1) Load route data
(2) Load shapes data
(3) Load disruption data
        
(4) Print shape IDs for a route
(5) Print coordinates for a shape ID
(6) Find longest shape for route
        
(7) Save routes and shapes in a pickle
(8) Load routes and shapes from a pickle
        
(9) Interactive map
(0) Quit
        """)

        try:
            user_input = int(input('Enter a command: ')) # Will result in an error if input is not a number since it changes input to an int
        except ValueError: 
            user_input = None # Updates variable to none, when it checks if variable is in the valid list, it will print error message since None is not valid
        except UnboundLocalError:
            user_input = None        

        if user_input not in [1, 2, 3, 4, 5, 6, 7, 8 ,9, 0]:
            print("Invalid option")
        if user_input == 0: # end loop
            quit = True
            return
        if user_input == 1:
            route_data = input1() # uses helper function, input1() --> stores {"route #": {"route_name": "Abbottsfield - Downtown - University", "shape_ids": {"008-210-South", "xxx"...}}}
        if user_input == 2:
            shapes_data = input2() # uses helper function, input2() --> stores {shape id: [[lat, lon]]} each lat lon is stored in its own list within the list of all lat, lons -> saved in order
        if user_input == 3: 
            disruption_data = input3() # uses helper function, input3() --> stores {2026-09-30: 53.425074385191095, -113.58983573962888}

        if user_input == 4: 
            try:
                print_shape_id(route_data) # uses helper function -> prints shape id of user inputted route number
            except UnboundLocalError: # Error checking, will trigger error since it tries to access route_data but it does not exist yet
                print("Route data hasn't been loaded yet")
        if user_input == 5:             
            try:
                print_coords(shapes_data) # uses helper function -> prints coordinates of user inputted shape_id
            except UnboundLocalError: # Error checking, will trigger error since it tries to access shapes_data but it does not exist yet
                print("Shape ID data hasn't been loaded yet")

        if user_input == 6:
            try:
                input6(route_data, shapes_data)
            except UnboundLocalError: # Error checking, will trigger error since it tries to access route_data but it does not exist yet
                print("Route data hasn't been loaded yet")

        if user_input == 7:
            try:
                input7(route_data, shapes_data, disruption_data)
            except UnboundLocalError: 
                print("Route data and Shape ID has not been loaded yet")
        if user_input == 8:
            route_data, shapes_data, disruption_data = input8()
        if user_input == 9:
            try:
                input9(route_data, shapes_data, disruption_data)
            except UnboundLocalError:
                print("Necessary data has not been loaded yet")

if __name__ == '__main__':
    main()
