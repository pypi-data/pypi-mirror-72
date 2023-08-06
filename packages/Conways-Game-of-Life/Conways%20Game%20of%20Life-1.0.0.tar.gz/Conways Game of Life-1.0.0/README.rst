# 2-Player Conways Game Of Life

You can play the game by clicking on this [repl link](https://repl.it/@Yonipineda/Game-of-Life#readme.md)

This is a project for my Computer Science build week at [Lambda School](https://lambdaschool.com/)

 
## Conways Game of Life: Help Screen 

Welcome to a 2-Player Game of Life implementation. Its true that this game is meant to be a 
zero-player game. You simply click start and you watch a wide range of patterns emerge, converge, 
die, and be born. Straight from wiki, the rules are as follow: 


    Conways Game of Life Rules: 

        The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of
        square cells, each of which is in one of two possible states, live or dead,
        (or populated and unpopulated, respectively). Every cell interacts with its eight 
        neighbours, which are the cells that are horizontally, vertically, or diagonally. 
        At each step in time, the following transitions occur:

        --- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        --- Any live cell with two or three live neighbours lives on to the next generation.
        --- Any live cell with more than three live neighbours dies, as if by overpopulation. 
        --- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.


        Thesse rules, which compare the behavior of the automation to real life, can be condensed 
        into the following:

        --- Any live cell with two or three live neighbours survives. 
        --- Any dead cell with three live neighbours becomes a live cell.
        --- All other live cells die in the next generation. Similarly, all other dead cells stay dead.


        The intial pattern consitutes the *seed* of the system. The generation is created by applying
        the above rules simultaneously to every cell in the seed; births and deaths occur  
        simultaneously, and the discrete moment at which this happenss is sometimes called a tick. 
        Each generation is a pure function of the preceding one. The rules continue to be applied 
        repeatedly to create further generations. 


This implementation is a tad different. Find more detail down below. 


## Conways Game of Life: 2-Player Version

This game has interactivity, additionally, you can play with a friend. It is based on the 
mechanics of the simulator, where players take it in turns to either place one of their own 
cells or kill any living cell. They can also choose to "Generate" the board, which is to say;
go forward a generation, at any point in *their* round. They don't have to use this ability,
it is optional and can decide to only use it once per round. 

The two available modes are as follow:

    --- 1 vs 1: Players try to get more of their *color* on the board. The winner is the one
                with the most color on the board after a pre-determined amount of turns or 
                who gets a certain amount first. 

    --- Survivor vs Entropy: One player is trying to get as many cells on the board while the 
                             other tries to kill them all. Additionally, the Survivor, being
                             the one placing cells, gets two turns for every turn Entropy, 
                             being the killer, gets.

Additional Options: 

    You can use options to add to the original mechanic, such as cells becoming immune after 
    being alive for a certain number of turns. You can also skip turns, saving that turn for the
    future. This will in turn, replace one of your oppenents cell with your own in the 
    next turn. 


Game Controls: 

    --- Press CTRL to use multiple turns in one. 
    --- Press ESC to deselect a cell when taking a turn. 
    --- Press F to show or hide what the board will look like in the next turn. 
    --- Press J to show or hide the amount of time cells have been alive for. 



## Help Menu 

General Controls: 

    --- LEFT CLICK to make a cell "alive".
    --- RIGHT CLICK to kill a cell. 
    --- Press ESC to exit the Main Menu. 


Simulator Controls:

    --- Press SPACE to pause/unpause the game. 
    --- Press RIGHT ARROW to move forward a single turn when paused. 
    --- Press ENTER to clear the board. 
    --- Presets(Found in the grid file): Press the corresponding number to execute a preset:

            ----1 - Glider 
            ----2 - Small Exploder 
            ----3 - Exploder 
            ----4 - Light Weight Space Ship 
            ----5 - Tumbler 
            ----6 - Gosper Glider Gun 
            ----7 - Pentadecathlon 
            ----8 - r-Pentomino 