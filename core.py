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
from typing import List, Tuple, Union
import json
from pathlib import Path
import cv2

class GameOfLife:
    
    def __init__(self, height: int = None, width: int = None, config: Union[str, Path] = None, alive_char: str = '#', dead_char: str = '-', dynamic: bool = True) -> None:
        assert (height and width) or config, 'You must provide grid dimensions or a configuration file.'
        self.width = width
        self.shape = (height, width,)
        if config:
            if isinstance(config, str):
                config = Path(config)
            self.load_conf(config)
        else:
            self.matrix = np.zeros(self.shape, dtype = bool)
        self.alive_char = alive_char
        self.dead_char = dead_char
        self.dynamic = dynamic

    def _clear_shell(self) -> None:
        _ = os.system('cls') if os.name == 'nt' else os.system('clear')

    def _rand_name(self, length) -> str:
        abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.sample(abc, length))

    def _reload_shape(self) -> None:
        self.shape = self.matrix.shape
    
    def _update_grid(self) -> None:
        """ Update the shape of the grid when a living cell come close to a border. """
        if not self.dynamic:
            return
        top_left_borders = [self.get_line(1), self.get_column(1)]
        bottom_right_borders = [self.get_line(self.shape[0] - 2), self.get_column(self.shape[1] - 2)]
        borders = [top_left_borders, bottom_right_borders]
        # y = 0 --> line
        # y = 1 --> column
        # i = 0 --> top-left borders
        # i = 1 --> bottom-right borders
        for i in range(2):
            for y, border in enumerate(borders[i]):
                shape = self.shape[0] if y == 1 else self.shape[1]
                if not any(border):
                    print('Not any')
                    continue
                print('Accessed')
                self.matrix = np.insert(self.matrix, self.shape[1] if i == 1 else i, np.zeros(shape, dtype = bool), axis = None if y == 0 else y)
        self._reload_shape()

    def get_matrix(self) -> np.array: return self.matrix 

    def get_cell(self, coords: Tuple[int]) -> Union[int, None]:
        x, y = coords
        try:
            self.matrix[x][y]
            return coords
        except IndexError:
            return None

    def get_line(self, line: int) -> List[bool]:
        return list(self.matrix[line])
    
    def get_column(self, column: int) -> List[bool]:
        return [self.matrix[i][column] for i in range(len(self.matrix))]

    def next_gen(self):
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
        self._update_grid()

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

    def run(self, wait_time: float = 0.1):
        """ Run the basic simulation. """
        import sys
        import time

        i = 1
        while 1:
            try:
                self._clear_shell()
                self.next_gen()
                print(f'\n\nGeneration [{i}]')
                print(self.view())
                print(self.shape)
                time.sleep(wait_time)
                i += 1
            except KeyboardInterrupt:
                self._clear_shell()
                sys.exit(1)

    def graphic_run(self):
        pass
                        
    def new_conf(self, path: Path = None) -> None:
        """ Generates a file to simplify default alive cells configuration. """
        if not path:
            path = Path(f'./{self._rand_name(10)}.gol')
        with open(path.absolute(), 'w') as f:
            f.writelines([str(list(self.matrix.astype(int)[i])) + '\n' for i in range(len(self.matrix))])

    def load_conf(self, path: Path) -> None:
        """ Loads a file containing the default configuration. """
        assert path.exists(), f'File \'{path.name}\' doesn\'t exist.'
        with open(path.absolute()) as f:
            conf = [json.loads(line) for line in f.readlines()]
        self.matrix = np.asarray(conf)
        self._reload_shape()

    def __repr__(self) -> str:
        return f'({self.shape} array) : \n{self.matrix.astype(int)}'

    def __str__(self) -> str:
        return self.__repr__()
        
if __name__ == '__main__':
    gol = GameOfLife(config = 'spaceship.gol')
    gol.run(wait_time = 0.005)