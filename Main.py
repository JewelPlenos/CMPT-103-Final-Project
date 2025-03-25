
# Load route data
def load_route(routefilename, tripsfilename) -> dict:
    '''
    Purpose: Read the data in routes.txt and trips.txt and store them in appropriate data structures 
    Parameters:
    Return:
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
            if route_id not in routes:
                routes[route_id] = {
                    'route_name': route_dict.get(route_id, None),
                    'shape_ids': set() 
                }
            routes[route_id]['shape_ids'].add(shape_id)
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
            coords = []
            parts = line.split(',')
            if parts[0] == 'shape_id': 
                continue # skip row 1 
            shapes_id, lat, lon = parts[0:3] #unpack parts into the needed variables
            coords.append(lat)
            coords.append(lon)
            if shapes_id not in shapes_data_dict:
                shapes_data_dict[shapes_id] = []
            shapes_data_dict[shapes_id] += [coords]   
    return shapes_data_dict

# Reserved for future use (Milestone 2)

# Main 
def main(): 
    quit = False 
    while not quit:
        print('Edmonton Transit System') 
        print('---------------------------------')
        print('(1) Load route data\n(2) Load shapes data\n(3) Reserved for future use\n\n(4) Print shape IDs for a route\n(5) Print coordinates for a shape ID\n(6) Reserved for future use\n\n(7) Save routes and shapes in a pickle\n(8) Load routes and shapes from a pickle\n\n(9) Reserved for future use\n(0) Quit\n')

        user_input = int(input('Enter a command: '))
        if user_input not in [1, 2, 3, 4, 5, 6, 7, 8 ,9, 0]:
            print("Invalid option")
        if user_input == 0: 
            quit = True
            return
        if user_input == 1:
            input_file = input('Enter a filename: ')
            split = input_file.split('/')
            try: 
                route_data = load_route(f'{split[0]}.txt', f'{split[1]}')
            except TypeError: 
                print(f"IO Error: couldn't open {input_file}")
                quit = True
            except IOError as fail: 
                print(f"IO Error: couldn't open {input_file}")
                quit = True

        shapes_data = load_shapes('shapes.txt')

if __name__ == '__main__':
    main()