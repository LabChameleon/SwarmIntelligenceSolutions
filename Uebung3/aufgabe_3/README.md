# Aufgabe 3

In the following we describe how the different behaviors of flocking are
implemented in our model:

* Each agent calculates the average direction of all neighbors in a certain range
* Each agent calculates its direction to the of mass direction of all neighbors in a 
certain range
* Each agent calculates the opposite direction of the center of mass of all neighbors in a 
certain range. This is to ensure that neighbors do not come to close.

All three directions are combined together with certain weights. It is important to give the 
avoidance direction a high weight in order to prevent clustering. The new direction corresponding
to the weight is then combined with the old direction of the agent and results in its new direction.

# Possible improvements

* use continuous grid
* use arrowheads for visualization of direction (continuous directions not supported yet)
* combination of new and old direction is done using a weighted sum. It would probably be more
smooth to always store the wanted new direction and adjust old direction slowly. Speed of this
adjustment can be corresponding to the angle between current direction and required direction.
