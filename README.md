(README not finished)
# Conway's Game of Life
Here's a pythonic version of Conway's game of life.
## Manual initialization
```python
gol = GameOfLife(height = 6, width = 10) # Creates a 10x10 grid.
gol.edit_state((3, 5), True)
gol.edit_state((2, 5), True)
gol.edit_state((1, 5), True)
print(gol.view())
```
*Result* : 
```
- - - - - - - - - -
- - - - - # - - - -
- - - - - # - - - -
- - - - - # - - - -
- - - - - - - - - -
- - - - - - - - - -
```
Then you can run the simulation with the `run` method : `gol.run()`.
## Config initialization
It's also possible to run the simulation through a configuration file defined using two characters only, that are then specified when initializing the `GameOfLife` object.

Example of configuration file (Glider Gun - `configs/glidergun.gol`) :
```
-----------------------------------------------------
-----------------------------------------------------
--------------------------#--------------------------
------------------------#-#--------------------------
--------------##------##------------##---------------
-------------#---#----##------------##---------------
--##--------#-----#---##-----------------------------
--##--------#---#-##----#-#--------------------------
------------#-----#-------#--------------------------
-------------#---#-----------------------------------
--------------##-------------------------------------
-----------------------------------------------------
-----------------------------------------------------
```
> *Note : Spaces are supported.* 

Then, in the python file :
```python
gol = GameOfLife(config = 'configs/glidergun.gol')
```
> *Note : When using a configuration file, the shape of the grid is automatically set.*

If you want to load a config with different alive and dead cell chars, you must specify a `custom_config` argument as so :
```python
gol = GameOfLife(config = 'configs/glidergun.gol', custom_config = {
    1: '@',
    0: '\''
}) # 1/0 or True/False can be used to specify alive and dead cell.
```
**Warning : this does not change the appearence of the cells in the console !** You must use the `alive_char` and `dead_char` arguments for this. 
## Random initialization
If you ever want to load a random simulation with a defined size, you can provide the special '`__random__`' keyword for the `config` argument. 
```python
gol = GameOfLife(config = '__random__', height = 30, width = 20)
```

## Graphic view
It's not always very practical to use the console to view the simulation. That's why this class provides a graphic view of the simulation. To use it, the `PyQt5` library as well as the `pyqtgraph` library must be installed.

Example with a random simulation :
```python
gol = GameOfLife(config = '__random__', height = 30, width = 20, graphic = True)
```