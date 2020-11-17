import requests
import sys
import argparse
from pprint import pprint
from tabulate import tabulate

# Method to printList in a tabulated format
def printList(moves,move_len):
    moves_formatted=[moves[x:x+5] for x in range(0, move_len, 5)]
    print(tabulate(moves_formatted,tablefmt="plain")) 

# Main function to invoke pokemon and check for lookups 
def pokemonMain():
    moves = []
    parser = argparse.ArgumentParser() 
     # Add long and short argument
    parser.add_argument("--lookup", "-l", help="set lookup")
    parser.add_argument("--generation", "-g", help="set generation")
    parser.add_argument("--move-type", "-m", help="set move-type generation")
    args = parser.parse_args()
    
    # Store values of arguments
    lookupValue = args.lookup
    generationValue = args.generation
    movetypeValue=args.move_type
   
    # Conditional statement to accept lookup for Pokedex or Pokemon name
    if lookupValue:
        try:
            if lookupValue.isdigit():
                input_type = "Pokedex" 
            else:
                input_type = "Pokemon name"
            url="https://pokeapi.co/api/v2/pokemon/"+lookupValue
            response = requests.get(url).json()  
                     
        # If requested resource is not present, notify and exit gracefully
        except ValueError as e: 
            print("No Pokemon exists with "+input_type + ":" + lookupValue+".")
            sys.exit()

        # Conditional statements to check the --generation flag and print moves accordingly   
        pokemonName = response['name']
        if generationValue:
            moves = generationEnabled(response,pokemonName,generationValue)        # Returns moves when generation flag is enabled 
        else:
            moves = generationDisabled(response,pokemonName)                       # Returns moves when generation flag is disabled
        if len(moves)== 0:
            print ("Pokemon "+ pokemonName + " does not appear in generation "+ generationValue +".")
        else :
            print("Pokemon Name : "+ pokemonName)
            print("Pokedex : "+ str(response['id']))
            print("Moves: ")
            move_len = len(moves)
            moves=sorted(moves)
            printList(moves,move_len)
    
    # Conditional statement to lookup moves by type
    if movetypeValue:
        moveType(movetypeValue,generationValue)

def moveType (movetypeValue,generationValue):
    moveList = [] 
    print_moves =True                                                           # Use a flag which is set to true if given moves are present for a type
    try:
        url_move_type= "https://pokeapi.co/api/v2/type/" + movetypeValue
        response_move_type=requests.get(url_move_type).json()
        generation_url = response_move_type['generation']['url']
        if generationValue:
            generation_type=requests.get(generation_url).json()
            version_group = generation_type['version_groups']
            for i in version_group:
                if i['name'] == generationValue:
                    print_moves=True
                    break
                else:
                    print_moves =False

    # If requested resource is not present, notify and exit gracefully
    except ValueError as e:  
        print("The move type "+movetypeValue + " is invalid. Please enter a valid move type")
        sys.exit()
    if  print_moves == True:    
        moveList= response_move_type['moves']
        moves= [x['name'] for x in moveList[0:10]]
        move_len = len(moves)
        printList(moves,move_len)
    else:
        print("There are no moves of given type in generation " + generationValue )

def generationEnabled(response,pokemonName,generationValue):
    moves = []
    try:
        url_generation="https://pokeapi.co/api/v2/pokemon-color/"+ generationValue
        response_generation=requests.get(url_generation).json()
    
        species_len = len(response_generation['pokemon_species'])
        moves_len = len(response['moves'])
        matched = False
        for i in range(0,species_len):
            species_temp=response_generation['pokemon_species'][i]['name']        # Append species name in a temporary variable
            
            if species_temp==pokemonName:
                matched=True
        
        
        if matched ==True:                                                                     # If matched append appropriate values to the moves list and return
            for i in range(0,moves_len):
                move_name=response['moves'][i]['move']['name']
                for j in response['moves'][i]['version_group_details']:
                    move_temp = j['version_group']['name']
                    if move_temp ==generationValue:
                        moves.append(move_name)
    except ValueError as e: 
        print("The generation " + generationValue + " does not exist")
        sys.exit()
    
    
    return moves
    
def generationDisabled(response,pokemonName):                                              # If generation flag is disabled append values to moves list and return
    moves = []
    moves_len = len(response['moves'])
    for i in range(0,moves_len):
        moves.append(response['moves'][i]['move']['name'])
    return moves
    
def main():  
    pokemonMain()

if __name__ == "__main__":
    main()