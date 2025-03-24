print('Edmonton Transit System') 
print('---------------------------------')
print('(1) Load route data\n(2) Load shapes data\n(3) Reserved for future use\n\n(4) Print shape IDs for a route\n(5) Print coordinates for a shape ID\n(6) Reserved for future use\n\n(7) Save routes and shapes in a pickle\n(8) Load routes and shapes from a pickle\n\n(9) Reserved for future use\n(0) Quit\n\nEnter Command: 0\n')

# Load route data
def load_route(filename):
    route_dict = {}
    with open(filename, 'r') as file: 
        for line in file: 
            parts = line.split(',') 
            route_dict[parts[0]] = parts[3]
    return route_dict

# Load shapes data

# Reserved for future use (Milestone 2)

# Main 
def main(): 
    route_data = load_route('routes.txt')

if __name__ == '__main__':
    main()