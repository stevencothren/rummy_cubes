# rummy_cubes
This project is a framework that lets you test AIs for the game Rummy Cubes.

To build your own AI you need to implement the player_ai function.  
This function will be passed 3 parameters  
- game_board  
        A list of "tile sets" which represent the tiles that have already been played  
- player_hand  
        A list of tiles that belong to your player  
- first_move  
        A boolean to signal whether or not you have played tiles  
            Your 1st move must have a point total >= 30, so this allows you to account for that  


The function needs to return a list of tile id lists.  
    Each tile id list represents a "tile set" that you want to add to the game board.  
    This can include tiles that are currently on the board and tiles that are in your hand.  
    Returning an empty or invalid list will result in a tile being drawn and added to your hand  
    
A tile is a dict and has the following keys  
- id  
    Randomly generated number that uniquely references a tile  
- suit  
    One of 'Black', 'Blue', 'Red' or 'Yellow'  
- value  
    The value of the tile (1 - 13)  
     Note: Jokers are currently disabled!  
        
A tile set is a list of tiles  
    
player_1.py is my work in progress attempt at an AI. It is currently pretty basic, but  
is able to play a game to completion from time to time.  

player_2.py currently just calls the player_1 AI to get it's moves.  

You can replace player_2.py with your own AI and it will automatically be included in the game.  
If you want to add additional players then the files should be name player_#.py  
where # is the next numeric player number.  
And you will need to set number_of_players accordingly in rummy_cubes.py  

By default, the framework will only play 1 game at a time.  
You can change number_of games in rummy_cubes.py to have it play multiple back-to-back games. 

This framework is still very new, so bugs are certainly possible.  

TODO
 - [ ] Support for Jokers in the framework  
 - [ ] Better (easier to read) printing of game board, player hand and player moves  
 - [ ] Automatically include all player_#.py files in the local directory as players in the game  
 - [ ] Track # of wins for multi-game runs  
 - [ ] Enhance Player 1 AI  
 - [ ] Build an 'AI' file that prompts the user for moves  
 - [ ] General refactoring and clean-up  