# ------------------------------- # 
# Group members: Jewel Plenos, Tommy Tran 
# Programming Project - Milestone#1
# ------------------------------- #

from datetime import date

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
    date_location = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split(',')
            finish_date = parts[3].split(' ') # --> ['Sep', '30,', '2026']
            date_object = (date({finish_date[2]}, {finish_date[0]}, {finish_date[1].strip(',')})) # --> (year, month, day)
            location = parts[-1] # --> POINT (-113.58983573962888 53.425074385191095)
            
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
        print(f'Data from {input_file} loaded\n')
        return route_data 

    except TypeError: 
        return print(f"IO Error: couldn't open {input_file}\n")
    except IOError as fail: 
        return print(f"IO Error: couldn't open {input_file}\n")
    except IndexError: # Index error happens when you try to input shapes.txt instead of trips.txt
        return print(f"IO Error: couldn't open {input_file}\n")

    

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
        print(f"Data from {input_shapes} loaded\n")
        return shapes_data
    except TypeError: 
        return print(f"IO Error: couldn't open {input_shapes}\n")
    except IOError as fail: 
        return print(f"IO Error: couldn't open {input_shapes}\n")    
    except IndexError: # Index error happens when you try to input trips.txt instead of shapes.txt
        return print(f"IO Error: couldn't open {input_shapes}\n")


def input3(): # Helper function when input == 3
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
        return print('\t** NOT FOUND **\n')
    
def print_coords(shapes_data): # Helper function when input == 5 
    '''
    Purpose: Gets user input on specific shape id, prints every corresponding coordinate 
    Parameter: shapes_data --> stores {shape id: [[lat, lon]]} each lat lon is stored in its own list within the list of all lat, lons -> saved in order
    Return: Error message or prints coords
    '''
    input_id = input("Enter shape ID: ").strip()

    try:
        print(f'Shape id coordinates for {input_id} are:\n')
        for item in shapes_data[input_id]: 
            print(f'\t({item[0]}, {item[1]})')
        print()
    except KeyError:
        return print('\t** NOT FOUND **\n')

def option6(): # Helper function when input == 6
    # Reserved for milestone 2 
    pass 

def option7(route_data, shapes_data): # Helper function when input ==  7
    '''
    Purpose: Save routes and shapes into a pickle file
    Parameter: route_data, dict containing route data
    shapes_data, dict containing shapes data
    Return: None
    '''
    import pickle
    filename = input("Enter a filename: ").strip()
    if filename == "":  # If filename empty use default name
        filename = "etsdata.p"
    
    try:  
        with open(filename, 'wb') as f:  # Write to file in binary
            pickle.dump({"route_data": route_data, "shapes_data": shapes_data}, f)  # Serialize and save dict
        print(f"Data structures successfully written to {filename}\n")
    except Exception as e:  # Return error if any issues arise
        print(f"Error writing to file: {e}\n")
 
def option8(): # Helper function when input == 8
    # Load routes and shapes from a pickle
    pass

def option9(): # Helper function when input == 9
    # Reserved for milestone 2
    pass


# Main 
def main(): 
    quit = False 
    while not quit:
        print('Edmonton Transit System') 
        print('---------------------------------')
        print('(1) Load route data\n(2) Load shapes data\n(3) Reserved for future use\n\n(4) Print shape IDs for a route\n(5) Print coordinates for a shape ID\n(6) Reserved for future use\n\n(7) Save routes and shapes in a pickle\n(8) Load routes and shapes from a pickle\n\n(9) Reserved for future use\n(0) Quit\n')

        try:
            user_input = int(input('Enter a command: ')) # Will result in an error if input is not a number since it changes input to an int
        except ValueError: 
            user_input = None # Updates variable to none, when it checks if variable is in the valid list, it will print error message since its not valid
        except UnboundLocalError:
            user_input = None        
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
            try:
                print_coords(shapes_data) # uses helper function -> prints coordinates of user inputted shape_id
            except UnboundLocalError: # Error checking, will trigger error since it tries to access shapes_data but it does not exist yet
                print("Shape ID data hasn't been loaded yet\n")
        if user_input == 7:
            try:
                option7(route_data, shapes_data)
            except UnboundLocalError: 
                print("Route data and Shape ID has not been loaded yet\n")

if __name__ == '__main__':
    main()
