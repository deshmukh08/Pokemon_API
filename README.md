# Pokemon API CLI

## Overview
This repository contains source code for the Python CLI which uses simple REST Pokemon API

## Requirements
To install all the requirements, simply run:
```
./requirements.txt
```
This will install all the required tools to run the CLI tool

## To run all commands
To run all commands in a single command run the following command:
```
./commands.txt
```
## To run single command
To run a single command run the following format:
```
python pokemon.py <item_to_lookup> < PokemonName/Pokedex/Move_Type>
```
## Implementation
Implemented the CLI by using the parameters passed as the command line argument, picked up the parameters like the lookup value, generation flag and move argument and saved the values. Further, considering the arguments passed, used REST calls to get the required list of Pokemon Name, Pokedex, Moves e.t.c. Considering the response required by the command, used Python datatypes to traverse through the data and append the required values by matching the conditions i.e. checking for the Pokemon name in a generation value like yellow. Handled the error gracefully if the resource was not found.
