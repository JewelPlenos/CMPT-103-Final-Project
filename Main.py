
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
        print(f'Data from {input_file} loaded\n')
        return route_data 

    except TypeError: 
        return print(f"IO Error: couldn't open {input_file}\n")
    except IOError as fail: 
        return print(f"IO Error: couldn't open {input_file}\n")
    

def input2(): # Helper function for input == 2 
    '''
    Purpose:
    Parameter:
    Return:
    '''
    input_shapes = input('Enter a filename: ').strip()
    try: 
        if input_shapes == '':
            input_shapes = 'data/shapes.txt'
        shapes_data = load_shapes(f'{input_shapes}') # Utilizes load_shapes helper function
        print(f"Data from {input_shapes} loaded\n")
        return shapes_data
    except TypeError: 
        return print(f"IO Error: couldn't open {input_shapes}\n")
    except IOError as fail: 
        return print(f"IO Error: couldn't open {input_shapes}\n")


def option3():
    '''
    Purpose:
    Parameter:
    Return:
    '''
# Reserved for future use (Milestone 2)
    pass 

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
    
def print_coords():
    '''
    Purpose:
    Parameter:
    Return:
    '''
    pass

# Main 
def main(): 
    quit = False 
    while not quit:
        print('Edmonton Transit System') 
        print('---------------------------------')
        print('(1) Load route data\n(2) Load shapes data\n(3) Reserved for future use\n\n(4) Print shape IDs for a route\n(5) Print coordinates for a shape ID\n(6) Reserved for future use\n\n(7) Save routes and shapes in a pickle\n(8) Load routes and shapes from a pickle\n\n(9) Reserved for future use\n(0) Quit\n')

        user_input = int(input('Enter a command: '))
        if user_input not in [1, 2, 3, 4, 5, 6, 7, 8 ,9, 0]:
            print("Invalid option\n")
        if user_input == 0: # end loop
            quit = True
            return
        if user_input == 1:
            route_data = input1() # uses helper function, input1() --> stores {"route #": {"route_name": "Abbottsfield - Downtown - University", "shape_ids": {"008-210-South", "xxx"...}}}
        if user_input == 2:
            shapes_data = input2() # uses helper function, input2() --> stores {shape id: [[lat, lon]]} each lat lon is stored in its own list within the list of all lat, lons -> saved in order
        if user_input == 4: 
            try:
                print_shape_id(route_data) # uses helper function -> prints shape id of user inputted route number
            except UnboundLocalError: # Error checking, will trigger error since it tries to access route_data but it does not exist yet
                print("Route data hasn't been loaded yet\n")
        if user_input == 5: 
            print_coords()
            pass

if __name__ == '__main__':
    main()