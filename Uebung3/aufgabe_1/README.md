# Observations for 40x40 field:

Use two different radius for measuring number of neighbors:
*	First, smaller radius, for deciding when to stop moving
* 	Second, larger radius, for deciding how long to wait considering
		the number of neighbors in larger radius

Increase wait time with a quadratic function, e.g. x^2, with input the number
of neighbors in larger radius. Quadratic function punishes small cluster more with
small wait times and favours large cluster. Exponetial functions favour larger
clusters sometimes too much (depends on the number of agents and the arena size). 
Thus, medium sized clusters may be stable independently from each other in some cases.
With linear functions small clusters can already take very long to collapse and hence make
it difficult for large clusters to form and stabilize. The function to calculate the waiting
time seems to be very important for success.

Small free walking steps make large clusters more stable.

First radius determines compactness and size of cluster. Second radius should have more or less the
size of the final large cluster according to second radius.

Choosing the right parameters gets more difficult for larger playing fields. Obviously the
larger the arena, the more difficult to create a single stable cluster with fixed number of agents.

# Implementations

* Model 1 only uses the two radiuses as described above with an exponential waiting function.
* Model 2 uses and quadratic waiting function but makes the agents walk to the center of gravity of
  their neighbours positions. 

