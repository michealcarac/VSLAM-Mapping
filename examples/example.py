# ------------------------------------------------------------------------------
# Name         : example.py
# Date Created : 2/22/2021
# Author(s)    : Chris Lloyd, Micheal Caracciola
# Github Link  : https://github.com/Clloyd3267/PyOccumap
# Description  : First example. CDL=> Add more later
# ------------------------------------------------------------------------------

# Internal Imports # CDL=> Figure out how to include across folders
from OccupancyGridMap import OccupancyGridMap

# External Imports
import time # Used to time exception speed

if __name__ == "__main__":
  print("Hello World!") # CDL=> Add more here
  start_time = time.time()
  grid_map = OccupancyGridMap()
  print("Done in: {:.2f}s".format(time.time() - start_time))