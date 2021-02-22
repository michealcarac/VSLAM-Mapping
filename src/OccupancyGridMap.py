# ------------------------------------------------------------------------------
# Name         : OccupancyGridMap.py
# Date Created : 2/22/2021
# Author(s)    : Chris Lloyd, Micheal Caracciola
# Github Link  : https://github.com/Clloyd3267/PyOccumap
# Description  : A simple occupancy grid map.
# ------------------------------------------------------------------------------

# Internal Imports

# External Imports

class OccupancyGridMap:
  """
  A class to implement a simple occupancy grid map.

  The occupancy grid is defined as a matrix of values. These values
  represent the likelyhood that a grid cell is occupied or not.

  Values between (0 - 1) indicate the value of occupancy. Within that
  range, whether a cell is considered occupied, is dependant on a whether
  it is greater than a certain threshold (cell_threshold).
  If these values are out of a specific range, or specifically -1, they are
  considered unknown or unvisited.

  A cell is occupied if its value >= occupancy_threshold.

  Each cell represents a physical square of area with a specified size:

  length = width = (cell_size)

  This allows to go between coordinates and actual position.

  Attributes:
    grid_map (matrix of float32): The occupancy grid map cell data.
    cell_threshold (float32):     The threshold to determine if a cell is
                                  occupied or not.
    cell_size (float32):          The unitless size that a single cell
                                  (width and height) represents.
    debug (bool):                 A variable to enable/disable debug outputs.
  """

    def __init__(self, _grid_map=[], _cell_threshold=0.5, _cell_size=1, _debug=0):
      """
      The default constructor for class OccupancyGridMap.

      Arguments:
        _grid_map (matrix of float32): A datamap to use as the gridmap.
        _cell_threshold (float32):     The threshold for a cell being occupied
        _cell_size (float32):          The unitless size of a cell's length and width.
        _debug (bool):                 Whether debug outputs are enabled.
      """

      self.grid_map       = _grid_map
      self.cell_threshold = _cell_threshold
      self.cell_size      = _cell_size
      self.debug          = _debug

  # ----------------------------------------------------------------------------
  # Class Methods
  # ----------------------------------------------------------------------------
  # CDL=> Here: List of methods
  #
  # getDataLoc(self, loc_point)
  # getDataIndex(self, index_point)
  # setDataIndex(self, index_point, value)
  # setDataLoc(self, loc_point, value)
  # isOccupiedLoc(self, loc_point)
  # isOccupiedIndex(self, index_point)
  # indexToLoc(self, index_point)
  # locToIndex(self, loc_point)
  # visualizeGrid(self, config)

if __name__ == "__main__":
  print("Hello World!") # CDL=> Add simple example of class