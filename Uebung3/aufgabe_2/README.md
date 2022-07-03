# Dispersion

# Exercise A

Basic approach I implemented only considers direction:
* calculate average direction to all neighbors 
* move to opposite direction of all neighbors

Approach can be improved by calculating weighted average with weights 
1/(distance to agent). However for large arenas this does not
make a difference in the final outcome when each agent has maximal distance in the end. 
For small arenas, were the whole area can be covered by agents, it may improve
results (I havent tested)

If the agent is only able to see distances, move to direction where distance
increases the most. This direction can be infered by jiggling around a little
bit.

# Exercise B

If agents do not have to see each other they can increase distance as much as they want.
If agents do have to keep contact they have to make sure they do not lose contact, e.g. making
sure a certain distance between them is not exceeded.

To ensure such a fully connected graph:
* Calculate minimal spanning tree of graph with distances of agents. Then do dispersion
in such a way that agents do not loose contact to their spanning tree neighbors. Requieres 
agents to be able to recognize each other. Minimal spanning tree can be calculated, starting
from one agent, with prims algorithm. 
Maybe allow updating of tree during dispersion to achieve better coverage. Updating can be done
with depth search first.
