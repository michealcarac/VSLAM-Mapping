# ------------------------------------------------------------------------------
# Name         : OccupancyGridMap.py
# Date Created : 2/22/2021
# Author(s)    : Chris Lloyd, Micheal Caracciolo
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
      loc_point (tuple of float32): A real world point (x, y). Scaled by cell_size.

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
      index_point (tuple of int): An indexed point (x, y).

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
      loc_point (tuple of float32): A real world point (x, y). Scaled by cell_size.
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
      index_point (tuple of int): An indexed point (x, y).
      value (float32):            The value of occupancy to set.

    Returns:
      value (float32): The value of occupancy.
    """

    # Ensure the point is valid
    if (not self.isValidIndexPoint(index_point)):
      print("ERROR: Entered point is invalid!")
      return -1 # CDL=> Should be exception thrown?

    # Get index point x,y
    x, y = index_point

    # Ensure the value is valid
    if (not self.isValidValue(value)):
      print("ERROR: Entered value is invalid!")
      return -1 # CDL=> Should be exception thrown?

    # Set the occupancy value
    self.grid_map[y][x] = value

    return value

  def isOccupiedLoc(self, loc_point):
    """
    Method to check if coordinate point is occupied.

    Args:
      loc_point (tuple of float32): A real world point (x, y). Scaled by cell_size.

    Returns:
      status (bool): Whether the position is occupied.
    """

    # Get the index of the given point
    index_point = self.locToIndex(loc_point)

    # Get occupied status
    return self.isOccupiedIndex(index_point)

  def isOccupiedIndex(self, index_point):
    """
    Method to check if index point is occupied.

    Args:
      index_point (tuple of int): An indexed point (x, y).

    Returns:
      status (bool): Whether the position is occupied.
    """

    # Ensure the point is valid
    if (not self.isValidIndexPoint(index_point)):
      print("ERROR: Entered point is invalid!")
      return -1 # CDL=> Should be exception thrown?

    # Get index point x,y
    x, y = index_point

    # Get the occupancy value
    value = self.grid_map[y][x]

    # Get occupied status
    return (cell_threshold <= value <= 1)

  def isUnoccupiedLoc(self, loc_point):
    """
    Method to check if coordinate point is unoccupied.

    Args:
      loc_point (tuple of float32): A real world point (x, y). Scaled by cell_size.

    Returns:
      status (bool): Whether the position is unoccupied.
    """

    # Get the index of the given point
    index_point = self.locToIndex(loc_point)

    # Get occupied status
    return self.isUnoccupiedIndex(index_point)

  def isUnoccupiedIndex(self, index_point):
    """
    Method to check if index point is unoccupied.

    Args:
      index_point (tuple of int): An indexed point (x, y).

    Returns:
      status (bool): Whether the position is unoccupied.
    """

    # Ensure the point is valid
    if (not self.isValidIndexPoint(index_point)):
      print("ERROR: Entered point is invalid!")
      return -1 # CDL=> Should be exception thrown?

    # Get index point x,y
    x, y = index_point

    # Get the occupancy value
    value = self.grid_map[y][x]

    # Get occupied status
    return (0 <= value <= cell_threshold)

  def isUnknownLoc(self, loc_point):
    """
    Method to check if coordinate point is unknown.

    Args:
      loc_point (tuple of float32): A real world point (x, y). Scaled by cell_size.

    Returns:
      status (bool): Whether the position is unknown.
    """

    # If not occupied or unoccupied, then unknown
    return not (isOccupiedLoc(loc_point) or isUnoccupiedLoc(loc_point))

  def isUnknownIndex(self, index_point):
    """
    Method to check if index point is unknown.

    Args:
      index_point (tuple of int): An indexed point (x, y).

    Returns:
      status (bool): Whether the position is unknown.
    """

    # If not occupied or unoccupied, then unknown
    return not (isOccupiedIndex(index_point) or isUnoccupiedIndex(index_point))

  def isValidValue(self, value):
    """
    Method to check if a value is valid.

    Args:
      value (float32): A occupancy value to check.

    Returns:
      status (bool): Whether the value is valid.
    """

    return True # CDL=> Implement later

  def isValidLocPoint(self, loc_point):
    """
    Method to check if coordinate point is valid.

    Args:
      loc_point (tuple of float32): A real world point (x, y). Scaled by cell_size.

    Returns:
      status (bool): Whether the position is valid.
    """

    # Get the index of the given point
    index_point = self.locToIndex(loc_point)

    # Check if point is valid
    return self.isValidIndexPoint(index_point)


  def isValidIndexPoint(self, index_point):
    """
    Method to check if index point is valid.

    Args:
      index_point (tuple of int): An indexed point (x, y).

    Returns:
      status (bool): Whether the position is valid.
    """

    # Get index point x,y
    x, y = index_point

    # Ensure the point is valid # CDL=> Check if conditional works
    return ((x < 0) or
            (y < 0) or
            (np.size(self.grid_map, 1) <= x) or
            (np.size(self.grid_map, 0) <= y))

  def locToIndex(self, loc_point):
    """
    Method to convert a coordinate point to an index point.

    Args:
      loc_point (tuple of float32): A real world point (x, y). Scaled by cell_size.

    Returns:
      index_point (tuple of int): An indexed point (x, y).
    """

    return tuple(axis*self.cell_size for axis in loc_point)


  def indexToLoc(self, index_point):
    """
    Method to check if index point is valid.

    Args:
      index_point (tuple of int): An indexed point (x, y).

    Returns:
      loc_point (tuple of float32): A real world point (x, y). Scaled by cell_size.
    """

    return tuple(int(round(axis/self.cell_size)) for axis in index_point)

  # CDL=> Here: List of methods
  #
  # [X] getDataLoc(self, loc_point)
  # [X] getDataIndex(self, index_point)
  # [X] setDataLoc(self, loc_point, value)
  # [X] setDataIndex(self, index_point, value)

  # [X] isOccupiedLoc(self, loc_point)
  # [X] isOccupiedIndex(self, index_point)
  # [X] isUnoccupiedLoc(self, loc_point)
  # [X] isUnoccupiedIndex(self, index_point)
  # [X] isUnknownLoc(self, loc_point)
  # [X] isUnknownIndex(self, index_point)

  # [X] isValidValue(self, value)
  # [X] isValidLocPoint(self, loc_point)
  # [X] isValidIndexPoint(self, index_point)
  # [X] indexToLoc(self, index_point)
  # [X] locToIndex(self, loc_point)

  # [ ] visualizeGrid(self, config)
  # [ ] fromCSV()

if __name__ == "__main__":
  print("Hello World!") # CDL=> Add simple example of class