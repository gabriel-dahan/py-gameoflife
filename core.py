'''
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, alive or dead, or "populated" or "unpopulated".
Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent.
At each step in time, the following transitions occur:

******************************************************************************************************
   1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
   2. Any live cell with two or three live neighbours lives on to the next generation.
   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
*******************************************************************************************************

The initial pattern constitutes the seed of the system.

The first generation is created by applying the above rules simultaneously to every cell in the seed—births and deaths occur simultaneously,
and the discrete moment at which this happens is sometimes called a tick (in other words, each generation is a pure function of the preceding one).

The rules continue to be applied repeatedly to create further generations.
'''

import os
import random
import numpy as np
from typing import Dict, Tuple, Union
import json
from pathlib import Path


class GameOfLife:
    
    def __init__(self, height: int = None, width: int = None, config: Union[str, Path] = None, alive_char: str = '#', dead_char: str = '-', custom_config: Dict[bool, str] = None, graphic: bool = False) -> None:
        assert (height and width) or config, 'You must provide grid dimensions or a configuration file.'
        self.graphic = graphic
        self.width = width
        self.shape = (height, width,) if height and width else None
        if config and config != '__random__':
            if isinstance(config, str):
                config = Path(config)
            if custom_config:
                self.load_conf(config, custom_config)
            else:
                self.load_conf(config)
            self.config = config
        elif config == '__random__':
            self.__random_conf(self.shape)
        else:
            self.matrix = np.zeros(self.shape, dtype = bool)
            self.config = None
        self.alive_char = alive_char
        self.dead_char = dead_char

    def __clear_shell(self) -> None:
        _ = os.system('cls') if os.name == 'nt' else os.system('clear')

    def __rand_name(self, length) -> str:
        abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
        return ''.join(random.sample(abc, length))

    def __reload_shape(self) -> None:
        self.shape = self.matrix.shape

    def __update_grid(self) -> None:
        """ Update the shape of the grid when a living cell come close to a border. """
        if any(self.matrix[1, i] for i in range(self.shape[1])):
            self.matrix = np.insert(self.matrix, 0, 0, axis = 0)
            self.__reload_shape()
        if any(self.matrix[-2, i] for i in range(self.shape[1])):
            self.matrix = np.append(self.matrix, [[0] * self.shape[1]], axis = 0)
            self.__reload_shape()
        if any(self.matrix[j, 1] for j in range(self.shape[0])):
            self.matrix = np.insert(self.matrix, 0, 0, axis = 1)
            self.__reload_shape()
        if any(self.matrix[j, -2] for j in range(self.shape[0])):
            self.matrix = np.append(self.matrix, [[0] for _ in range(self.shape[0])], axis = 1)
            self.__reload_shape()

    def get_matrix(self) -> np.ndarray: return self.matrix 

    def get_cell(self, coords: Tuple[int]) -> Union[int, None]:
        x, y = coords
        try:
            self.matrix[x][y]
            return coords
        except IndexError:
            return None

    def next_gen(self, update_grid: bool = False) -> None:
        if update_grid:
            self.__update_grid()
        int_matrix = self.matrix.astype(int)
        neigh = np.zeros(int_matrix.shape)
        neigh[1:-1, 1:-1] = (
            int_matrix[:-2, :-2]  + int_matrix[:-2, 1:-1] + int_matrix[:-2, 2:]  + 
            int_matrix[1:-1, :-2] +                         int_matrix[1:-1, 2:] + 
            int_matrix[2:, :-2]   + int_matrix[2:, 1:-1]  + int_matrix[2:, 2:]
        )
        self.matrix = np.logical_or(
            neigh == 3, 
            np.logical_and(int_matrix == 1, neigh == 2)
        )

    def edit_state(self, cell: Tuple[int], state: bool):
        x, y = cell
        self.matrix[x][y] = state

    def view(self) -> str:
        temp = self.matrix
        string = ''
        for line in temp:
            for cell in line:
                string += f'{self.alive_char} ' if cell else f'{self.dead_char} '
            string += '\n'
        return string

    def __shell_run(self, wait_time: float) -> None:
        import sys
        import time

        i = 1
        while 1:
            try:
                self.__clear_shell()
                self.next_gen()
                print(f'\n\nGeneration [{i}]')
                print(self.view())
                print(f'x: {self.shape[0]}\ny: {self.shape[1]}\n')
                time.sleep(wait_time)
                i += 1
            except KeyboardInterrupt:
                self.__clear_shell()
                sys.exit(1)

    def __graphic_run(self, wait_time: float) -> None:
        from graphic import GraphicGOL
        from pyqtgraph.Qt import mkQApp

        mkQApp("Game Of Life matrix display")
        graph = GraphicGOL(self)
        graph.run(wait_time)

    def run(self, wait_time: float = 0.1) -> None:
        """ Run the basic simulation. """
        if not self.graphic:
            self.__shell_run(wait_time)
        else:
            self.__graphic_run(wait_time)
                        
    def new_conf(self, path: Path = None) -> None:
        """ Generates a file to simplify default alive cells configuration. """
        if not path:
            path = Path(f'./{self.__rand_name(10)}.gol')
        with open(path.absolute(), 'w') as f:
            f.writelines([str(list(self.matrix.astype(int)[i])) + '\n' for i in range(len(self.matrix))])

    def load_conf(self, path: Path, custom_repr: Dict[bool, str] = None) -> None:
        """ Loads a file containing the default configuration. """
        assert path.exists(), f'File \'{path.name}\' doesn\'t exist.'
        with open(path.absolute()) as f:
            if custom_repr:
                conf = [line.strip('\n') for line in f.readlines()]
                for i in range(len(conf)):
                    conf[i] = [0 if val == custom_repr[False] else 1 for val in conf[i] if val != ' ']
            else:
                conf = [json.loads(line) for line in f.readlines()]
        self.matrix = np.asarray(conf)
        self.__reload_shape()

    def __random_conf(self, shape: Tuple[int] = None):
        """ Generates a random matrix for testing purposes. """
        self.matrix = np.random.choice(a = [0, 1], size = shape or (75, 75))
        self.__reload_shape()

    def __repr__(self) -> str:
        return f'GameOfLife(default_conf: "{self.config}", array: {self.shape})'

    def __str__(self) -> str:
        return self.__repr__()

if __name__ == '__main__':
    # gol = GameOfLife(config = 'configs/pulsar.gol', custom_config = {
    #     1: '#',
    #     0: '-'
    # }, graphic = True)
    ## gol = GameOfLife(config = '__random__', width = 75, height = 75, graphic = True)
    ## gol.run()
    #- gol = GameOfLife(height = 6, width = 10) # Creates a 10x10 grid.
    #- gol.edit_state((3, 5), True)
    #- gol.edit_state((2, 5), True)
    #- gol.edit_state((1, 5), True)
    #- print(gol.view())
    pass