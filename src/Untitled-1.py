from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from OccupancyGridMap import *

print("Loading map data")
ogm = OccupancyGridMap()
ogm.fromKeyframesCSV("../data/keyframes.csv")
print("Visualizing grid map data")
ogm.visualizeGrid()

matrix = ogm.grid_map
grid = Grid(matrix=matrix)

start = grid.node(0, 0)
end = grid.node(20, 7)

finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, runs = finder.find_path(start, end, grid)
print(path)
#print('operations:', runs, 'path length:', len(path))
#print(grid.grid_str(path=path, start=start, end=end))