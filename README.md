(README not finished)
# Conway's Game of Life
Here's a pythonic version of Conway's game of life.
## Run using python
```python
gol = GameOfLife(height = 6, width = 10) # Creates a 10x10 grid.
gol.edit_state((5, 5), True)
gol.edit_state((4, 5), True)
gol.edit_state((3, 5), True)
gol.run()
```
*Result* : 
```
----------
----------
----------
----------
----------
----------
```