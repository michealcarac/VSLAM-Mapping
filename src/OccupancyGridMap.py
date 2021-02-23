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

    Args:
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

  def getDataLoc(self, loc_point):
    """
    Method to get the occupancy value at a certain coordinate location.

    Args:
      loc_point (tuple of float32): A real world point (x, y). Scaled by _cell_size.

    Returns:
      value (float32): The value of occupancy.
    """

    # Get the index of the given point
    index_point = self.locToIndex(loc_point)

    # Get the value of occupancy
    return self.getDataIndex(index_point)

  def getDataIndex(self, index_point):
    """
    Method to get the occupancy value at a certain index location.

    Args:
      index_point (tuple of float32): An indexed point (x, y).

    Returns:
      value (float32): The value of occupancy.
    """

    # Ensure the point is valid
    if (not self.isValidIndexPoint(index_point)):
      print("ERROR: Entered point is invalid!")
      return -1 # CDL=> Should be exception thrown?

    # Get index point x,y
    x, y = index_point

    # Get the value of occupancy
    return self.grid_map[y][x]

  def setDataLoc(self, loc_point, value):
    """
    Method to set the occupancy value at a certain coordinate location.

    Args:
      loc_point (tuple of float32): A real world point (x, y). Scaled by _cell_size.
      value (float32):              The value of occupancy to set.

    Returns:
      value (float32): The value of occupancy.
    """

    # Get the index of the given point
    index_point = self.locToIndex(loc_point)

    # Set the occupancy value
    return setDataIndex(index_point, value)


  def setDataIndex(self, index_point, value):
    """
    Method to set the occupancy value at a certain index location.

    Args:
      index_point (tuple of float32): An indexed point (x, y).
      value (float32):                The value of occupancy to set.

    Returns:
      value (float32): The value of occupancy.
    """

    # Ensure the point is valid
    if (not self.isValidIndexPoint(index_point)):
      print("ERROR: Entered point is invalid!")
      return -1 # CDL=> Should be exception thrown?

    # Get index point x,y
    x, y = index_point

    # CDL=> Add logic to validate value

    # Set the occupancy value
    self.grid_map[y][x] = value

    return value










    # Get index point x,y
    x, y = index_point

    # Ensure the point is valid # CDL=> Check if conditional works
    if ((x < 0) or
        (y < 0) or
        (np.size(self.grid_map, 1) <= x) or
        (np.size(self.grid_map, 0) <= y)):



  # CDL=> Here: List of methods
  #
  # [X] getDataLoc(self, loc_point)
  # [X] getDataIndex(self, index_point)
  # [X] setDataLoc(self, loc_point, value)
  # [X] setDataIndex(self, index_point, value)
  # [ ] isOccupiedLoc(self, loc_point)
  # [ ] isOccupiedIndex(self, index_point)
  # [ ] isUnoccupiedLoc(self, loc_point)
  # [ ] isUnoccupiedIndex(self, index_point)
  # [ ] isUnknownLoc(self, loc_point)
  # [ ] isUnknownIndex(self, index_point)
  # [ ] isValidLocPoint(self, loc_point)
  # [ ] isValidIndexPoint(self, index_point)
  # [ ] indexToLoc(self, index_point)
  # [ ] locToIndex(self, loc_point)
  # [ ] visualizeGrid(self, config)
  # [ ] fromCSV()

if __name__ == "__main__":
  print("Hello World!") # CDL=> Add simple example of class