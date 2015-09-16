"""
Grids handling and setting functions.

This module defines various functions related to grid configurations and 
computations.
"""

import mamba.core as core

###############################################################################
#  Definitions

class _grid:
    def __init__(self, id, default=False):
        self.id = id
        self.default = default
        
    def __repr__(self):
        if self.id==core.MB_HEXAGONAL_GRID:
            return "HEXAGONAL"
        elif self.id==core.MB_SQUARE_GRID:
            return "SQUARE"
        else:
            return ""
            
    def __eq__(self, other):
        return self.id==other.id
    def __ne__(self, other):
        return self.id!=other.id
            

HEXAGONAL = _grid(core.MB_HEXAGONAL_GRID)
""" Value to be used when working on an hexagonal grid. """

SQUARE = _grid(core.MB_SQUARE_GRID)
""" Value to be used when working on a square grid. """

DEFAULT_GRID = _grid(core.MB_HEXAGONAL_GRID, True)
""" Value holding the default grid (set to HEXAGONAL at Mamba startup). """

class _edge:
    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        if self.id==core.MB_EMPTY_EDGE:
            return "EMPTY"
        elif self.id==core.MB_FILLED_EDGE:
            return "FILLED"
        else:
            return ""
            
    def __eq__(self, other):
        return self.id==other.id
    def __ne__(self, other):
        return self.id!=other.id

EMPTY = _edge(core.MB_EMPTY_EDGE)
""" Value to be used when setting an empty edge. """

FILLED = _edge(core.MB_FILLED_EDGE)
""" Value to be used when setting a filled edge. """

###############################################################################
# Public functions are functions dealing with grid, counter and such

def setDefaultGrid(grid):
    """
    This function will change the value of the default grid used in each 
    operator that needs to specify one.
    
    'grid' must be either HEXAGONAL or SQUARE.
    
    You can of course manually change the variable DEFAULT_GRID by yourself.
    Using this function is however recommended if you are not sure of what you 
    are doing.
    """
    if grid==HEXAGONAL or grid==SQUARE:
        DEFAULT_GRID.id = grid.id
    else:
        raise ValueError("Invalid grid for default")

def getDirections(grid=DEFAULT_GRID, withoutZero=False):
    """
    Returns a range of all the possible directions available in 'grid' 
    (set to DEFAULT_GRID by default). If 'withoutZero' is set to True, the
    direction 0 is omitted.
    
    If the 'grid' value is incorrect, the function returns an empty list.
    """
    if grid.id==core.MB_HEXAGONAL_GRID:
        return range(withoutZero and 1 or 0, 7, 1)
    elif grid.id==core.MB_SQUARE_GRID:
        return range(withoutZero and 1 or 0, 9, 1)
    else:
        return []

def gridNeighbors(grid=DEFAULT_GRID):
    """
    Returns the number of neighbors of a point in 'grid' (6 or 8).
    
    If the 'grid' value is incorrect, the function returns 0.
    """
    if grid.id==core.MB_HEXAGONAL_GRID:
        return 6
    elif grid.id==core.MB_SQUARE_GRID:
        return 8
    else:
        return 0

def rotateDirection(d, step=1, grid=DEFAULT_GRID):
    """
    Calculates the value of the new direction starting from direction 'd' after 
    'step' rotations (default value 1). If 'step' is positive, rotations are 
    performed clockwise. They are counterclockwise if 'step' is negative.
    Calculation is made according to the grid. Direction 0 is taken into account 
    (and always unchanged).
    """
    if d == 0:
        return 0
    else:
        return (d + step - 1)%gridNeighbors(grid) + 1

def transposeDirection(d, grid=DEFAULT_GRID):
    """
    Calculates the transposed (opposite) direction value of direction 'd' 
    (corresponds to a rotation of gridNeighbors/2 steps).
    """
    o = rotateDirection(d, gridNeighbors(grid)//2, grid)
    return o

