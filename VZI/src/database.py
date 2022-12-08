import sys
import json

from geopy.geocoders import Nominatim
from geopy import distance

class Nodes_Airports(object):
    def __init__(self, name_city):
        self.__locator(name_city)
    
    # private method:
    #   input: inputed name city
    #   return 
    def __locator(self, name_city):
        # set up geolocator from library geopy 
        geolocator = Nominatim(user_agent="VZI_project")
        val = False
        
        # geolocation of defined city
        location = geolocator.geocode(name_city, addressdetails=True, language='en')
        
        # if input city can be geolocated and if is to possible to set
        if location is None:
            raise ValueError("Put right name of City!")

        for i in location.raw['address']:
            if i == 'city':
                val = True
                break

        if not val:
            raise ValueError("Put right name of City!")
        
        new_node, county = location.raw['address']['city'], location.raw['address']['country']
        print('Do u have on mind: ' + location.raw['address']['city'] + ', ' + location.raw['address']['country'] + '?')
        
        con = input("Enter your value [y/n]: ") 
        if con == 'y' or con == 'Y':
            print(new_node + '-' + county + ' [' + 'latitude: ' + str(location.latitude) + ', longitude: ' + str(location.longitude) + ']')
            
            old_node = input("[INPUT] Add to node city in form City-Airport: ")

            # function call to validate and search the data file
            latitude_, longitude_ = self.__validation(new_node, old_node)

            # coordinate storage, where new_node_loc = new city(node), old_node_loc = already recorded city(node) 
            new_node_loc = [location.latitude, location.longitude]
            old_node_loc = [latitude_, longitude_]

            # time calculation as a parameter for the graph edge
            time = self.__calculator(new_node_loc, old_node_loc)

            # adding nodes and edges to the database
            self.__add_node(new_node, old_node, new_node_loc, time)

        else:
            print("[INFO] No City-Airport was choosed")
    
    # private method:
    #   input: add city, city, city location, time
    #   return 
    def __add_node(self, add_city, city, add_city_loc, time):
        # nodes are represented in the structure as city-Airport
        add_city = add_city + '-Airport'
        
        # creation of dictionaries for writing to external files
        data={add_city:{'lat': str(add_city_loc[0]), 'lon': str(add_city_loc[1]) }}
        data2 = {add_city:{city:time},}

        # write and update existing data in external files
        with open('data/airports_location.json', 'r+') as infile:
            locations = json.load(infile)

            infile.seek(0) 

            locations.update(data)
            json.dump(locations, infile, indent=2)

            infile.truncate()      
        infile.close()
        
        with open('data/flights_data.json', 'r+') as outfile:
            f_data = json.load(outfile)
            outfile.seek(0)
            
            if add_city in f_data.keys():
                f_data[add_city].update({city: time})
                f_data[city].update({add_city: time})

            else:
                f_data[city].update({add_city: time})
                f_data.update(data2)

            json.dump(f_data,outfile, indent=2)

            outfile.truncate()   
        outfile.close()

    # private method:
    #   input: node city 1, node city 2
    #   return 
    # Note: distance from two nodes, rounded and in units of km, divided by the velocity constant, which represents the average speed of the aircraft,​
    # also solves the validation if there is an already specified route, the function then returns the time as an edge parameter
    def __calculator(self, node_1, node_2):
        velocity = 515
        distance_airline = round(distance.distance(node_1, node_2).kilometers,0)
        time = int(round((distance_airline/velocity)*60,0))
        return time

    # private method:
    #   input: add city, search city
    #   return latitude, longitude
    # Note: The function validates whether the input values correspond to the values in the database and if necessary the coordinates are returned,
    # the function also solves if the correct input was entered to match the date in the external files, also solves the validation if there is an already specified route.
    def __validation(self, add_city, search_city):
        add_city = add_city+"-Airport"
                
        with open('data/flights_data.json', 'r') as outfile:
            distances = json.load(outfile)
        
        if not search_city in distances.keys():
            raise ValueError ("Put in form: 'City-Airport'")
        
        for i in distances[search_city].keys():
            if i == add_city:
                latitude = None
                longitude = None
                print("Sorry but this flight record already exists!!")
                break

        with open('data/airports_location.json', 'r') as outfile:
            locations = json.load(outfile)
        
        for i in locations.keys():
            if i == search_city:        
                latitude = locations[i]['lat']
                longitude = locations[i]['lon']
                
        return latitude, longitude

def main():
    while 1:
        try:
            print("[INFO] Do you want to quit?")
            con = input("[INPUT] Enter your value [y/n]: ") 
            
        except:
            raise KeyError("Wrong key interrupt!")
        
        if con == 'y' or con == 'Y':
            sys.exit()
        
        else:
            try:
                num = input("[INPUT] Choose city: ")
            except:
                raise KeyError("Wrong key interrupt!") 
            
            Nodes_Airports(num)

if __name__ == "__main__":
    main()