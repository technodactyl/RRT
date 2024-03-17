# RRT

## Implementation of RRT and RRT* algorithms in Python using pygame.

Instructions for running:
- Can be run on Python 3 in a virtual environment or out, as long as the latest version of pygame (2.5.2) is installed.
- If running from a terminal, navigate to RRT folder (this folder) and type the command 'python3 ./RRT.py' or 'python3 ./RRTStar.py' to execute.
- On running this, input prompts will show up. 
- The first input prompt is for choosing the method of generating start points and obstacles.
- Type 'i' and press Enter to input start and goal nodes and obstacles manually, or any other key followed by Enter to generate two random points and anywhere between 1 and 100 obstacles.
- The input order is as follows:
-- X-coordinate of the start node. (min 0, max 1028)
-- Y-coordinate of the start node. (min 0, max 534)
-- X-coordinate of the goal node. (min 0, max 1028)
-- Y-coordinate of the goal node. (min 0, max 534)
-- Number of obstacles (min 1, max 10)
-- For each obstacle:
--- X-coordinate of the obstacle. (min 0, max 1028)
--- Y-coordinate of the obstacle. (min 0, max 1028)
- Not sticking to the numbers will not break the code, but you will most likely not be able to see the nodes or the obstacles in the pygame window.
- After this, the corresponding scenario should run.

Changelog and issues
- Tested on Windows 11 using Visual Studio and Ubuntu 22.04
- Added maximum number of neighbors for a new node in RRT* to not waste compute time and resources. Can be changed by changing the "max_neighbors" variable in the RRT* program.
- Added "max_points" to put a limit on the maximum number of nodes that can be spawned.
- Paths may occasionally pass through obstacles in the RRT* implementation, only if two nodes are on different sides of an obstacle. This is due to not including collision detection in the connection optimization step so as to not increase compute time.
